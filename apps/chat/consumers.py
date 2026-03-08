# chat/consumers.py
import json
import re
import google.generativeai as genai
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message

WHATSAPP_NUMBER = '237674554947'

SYSTEM_PROMPT = """Tu es l'assistant virtuel de VisionTech SARL, une entreprise spécialisée dans la conception de systèmes d'intelligence artificielle, basée à Bafoussam, Cameroun.

VisionTech SARL conçoit et déploie des solutions IA sur-mesure :
- Chatbots et assistants virtuels intelligents
- Systèmes de vision par ordinateur et reconnaissance d'images
- Automatisation de processus métier par l'IA (RPA + AI)
- Analyse prédictive et modèles de machine learning
- Intégration d'IA dans les systèmes existants (ERP, CRM, web, mobile)
- Conseil et audit en transformation par l'intelligence artificielle

Localisation : Bafoussam, Région de l'Ouest, Cameroun.
Contact WhatsApp : +237 674 55 49 47

Règles de conduite :
- Réponds dans la langue de l'utilisateur : français si il écrit en français, anglais si il écrit en anglais
- Sois professionnel, chaleureux et concis (3-4 phrases max)
- Si on te demande ce que VisionTech ne fait pas (formations génériques, e-commerce sans IA), explique poliment la spécialisation IA
- Si la demande nécessite un devis, une démo ou une expertise approfondie, dis exactement : "Je vais vous mettre en contact avec un de nos conseillers."
- Ne dépasse jamais 4 phrases par réponse"""

TRANSFER_KEYWORDS = [
    'humain', 'agent', 'conseiller', 'parler à quelqu\'un',
    'urgence', 'problème grave', 'rappel', 'devis', 'prix', 'tarif',
    'démo', 'demonstration', 'rendez-vous', 'rdv', 'rencontre', 'appel'
]

def build_whatsapp_url(phone_number, conv_summary):
    """Génère un lien WhatsApp avec message pré-rempli."""
    msg = (
        f"Bonjour VisionTech 👋\n"
        f"Je vous contacte depuis le chat de votre site.\n\n"
        f"📋 Résumé de ma demande :\n{conv_summary}\n\n"
        f"Mon numéro : {phone_number}"
    )
    encoded = msg.replace(' ', '%20').replace('\n', '%0A')
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group = f'chat_{self.session_id}'
        self.waiting_for_phone = False  # état : on attend le numéro ?

        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

        self.conversation = await self.get_or_create_conversation()
        history = await self.get_history()
        await self.send(json.dumps({'type': 'history', 'messages': history}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('type', 'message')

        if msg_type == 'message':
            user_text = data.get('text', '').strip()
            if not user_text:
                return

            await self.save_message(user_text, 'user')
            await self.broadcast('user', user_text)

            conv_status = await self.get_conv_status()

            # ── Étape 2 : l'utilisateur donne son numéro ──────────────────────
            if self.waiting_for_phone:
                phone = self.extract_phone(user_text)
                if phone:
                    self.waiting_for_phone = False
                    await self.update_visitor_phone(phone)
                    await self.update_conv_status('pending')

                    # Résumé de la conversation pour le message WhatsApp
                    summary = await self.get_conv_summary()
                    wa_url = build_whatsapp_url(phone, summary)

                    # Sauvegarder le lien comme message bot
                    wa_msg = f"WHATSAPP_CARD::{wa_url}::{phone}"
                    await self.save_message(wa_msg, 'bot')

                    await self.send(json.dumps({
                        'type': 'whatsapp_card',
                        'wa_url': wa_url,
                        'phone': phone,
                    }))
                else:
                    # Numéro invalide, redemander
                    reply = "Je n'ai pas reconnu ce numéro. Merci d'entrer votre numéro WhatsApp avec l'indicatif (ex: 237 6XX XX XX XX)."
                    await self.save_message(reply, 'bot')
                    await self.broadcast('bot', reply)
                return

            # ── Mode bot normal ───────────────────────────────────────────────
            if conv_status == 'bot':
                needs_transfer = any(kw in user_text.lower() for kw in TRANSFER_KEYWORDS)
                reply = await self.get_gemini_response(user_text)
                await self.save_message(reply, 'bot')
                await self.broadcast('bot', reply)

                if needs_transfer or 'conseillers' in reply.lower():
                    await self.trigger_whatsapp_flow()

        elif msg_type == 'request_human':
            await self.trigger_whatsapp_flow()

    # ── Déclenche le flux WhatsApp ─────────────────────────────────────────────
    async def trigger_whatsapp_flow(self):
        self.waiting_for_phone = True
        ask_msg = (
            "📱 Pour vous mettre en contact avec un conseiller VisionTech, "
            "merci de nous indiquer votre numéro WhatsApp "
            "(avec indicatif pays, ex: 237 674 55 49 47) :"
        )
        await self.save_message(ask_msg, 'bot')
        await self.broadcast('bot', ask_msg)

    # ── Helpers broadcast ──────────────────────────────────────────────────────
    async def broadcast(self, sender, text):
        await self.channel_layer.group_send(self.room_group, {
            'type': 'chat_message',
            'sender': sender,
            'text': text,
        })

    async def chat_message(self, event):
        await self.send(json.dumps({
            'type': 'message',
            'sender': event['sender'],
            'text': event['text'],
        }))

    # ── Extraction numéro de téléphone ────────────────────────────────────────
    def extract_phone(self, text):
        """Extrait un numéro de téléphone africain/international du texte."""
        cleaned = re.sub(r'[\s\-\.\(\)]', '', text)
        # Formats : 237XXXXXXXXX, +237XXXXXXXXX, 6XXXXXXXX (Cameroun)
        patterns = [
            r'(\+?237[0-9]{8,9})',   # +237 ou 237 + 8-9 chiffres
            r'(\+?[0-9]{10,13})',    # International générique
        ]
        for pattern in patterns:
            match = re.search(pattern, cleaned)
            if match:
                number = re.sub(r'\+', '', match.group(1))
                return number
        return None

    # ── Gemini ────────────────────────────────────────────────────────────────
    async def get_gemini_response(self, user_text):
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=SYSTEM_PROMPT
            )
            history = await self.get_history()
            chat_history = []
            for m in history[-10:]:
                role = 'user' if m['sender'] == 'user' else 'model'
                chat_history.append({'role': role, 'parts': [m['text']]})

            chat = model.start_chat(history=chat_history)
            response = chat.send_message(user_text)
            return response.text
        except Exception as e:
            return f"Désolé, je rencontre un problème technique. ({str(e)[:60]})"

    # ── DB helpers ────────────────────────────────────────────────────────────
    @database_sync_to_async
    def get_or_create_conversation(self):
        conv, _ = Conversation.objects.get_or_create(session_id=self.session_id)
        return conv

    @database_sync_to_async
    def save_message(self, content, sender):
        return Message.objects.create(
            conversation=self.conversation,
            content=content,
            sender=sender
        )

    @database_sync_to_async
    def get_history(self):
        messages = Message.objects.filter(
            conversation=self.conversation
        ).order_by('timestamp')
        return [
            {
                'id': str(m.id),
                'sender': m.sender,
                'text': m.content,
                'timestamp': m.timestamp.isoformat(),
            }
            for m in messages
        ]

    @database_sync_to_async
    def get_conv_summary(self):
        """Résume les 5 derniers messages utilisateur pour le message WhatsApp."""
        messages = Message.objects.filter(
            conversation=self.conversation,
            sender='user'
        ).order_by('-timestamp')[:5]
        lines = [m.content for m in reversed(messages)]
        return ' | '.join(lines) if lines else 'Nouvelle demande'

    @database_sync_to_async
    def get_conv_status(self):
        self.conversation.refresh_from_db()
        return self.conversation.status

    @database_sync_to_async
    def update_conv_status(self, status):
        self.conversation.status = status
        self.conversation.save()

    @database_sync_to_async
    def update_visitor_phone(self, phone):
        self.conversation.visitor_email = phone  # réutilise le champ existant
        self.conversation.save()