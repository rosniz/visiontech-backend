# chat/consumers.py
import json
import google.generativeai as genai
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message


SYSTEM_PROMPT = """Tu es l'assistant virtuel de VisionTech, une entreprise tech basée à Douala, Cameroun.
VisionTech propose :
- Développement web & mobile sur-mesure
- Formations en programmation (Python, JavaScript, React, Django...)
- Consulting digital & transformation numérique
- Solutions e-commerce et ERP

Réponds toujours en français, sois professionnel, chaleureux et concis.
Si la demande est complexe ou urgente, propose de transférer à un agent humain en disant exactement : "Je vais vous mettre en contact avec un de nos conseillers."
Ne dépasse pas 3-4 phrases par réponse."""

TRANSFER_KEYWORDS = [
    'humain', 'agent', 'conseiller', 'parler à quelqu\'un',
    'urgence', 'problème grave', 'rappel', 'devis', 'prix', 'tarif'
]


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group = f'chat_{self.session_id}'

        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

        # Charger ou créer la conversation
        self.conversation = await self.get_or_create_conversation()

        # Envoyer l'historique au client
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

            # Sauvegarder message utilisateur
            await self.save_message(user_text, 'user')

            # Broadcast au groupe (utile si agent connecté aussi)
            await self.channel_layer.group_send(self.room_group, {
                'type': 'chat_message',
                'sender': 'user',
                'text': user_text,
            })

            conv_status = await self.get_conv_status()

            if conv_status == 'bot':
                # Vérifier si transfert demandé
                needs_transfer = any(kw in user_text.lower() for kw in TRANSFER_KEYWORDS)

                # Générer réponse Gemini
                reply = await self.get_gemini_response(user_text)
                await self.save_message(reply, 'bot')

                await self.channel_layer.group_send(self.room_group, {
                    'type': 'chat_message',
                    'sender': 'bot',
                    'text': reply,
                })

                # Vérifier si Gemini lui-même suggère un transfert
                if needs_transfer or 'conseillers' in reply.lower():
                    await self.update_conv_status('pending')
                    await self.channel_layer.group_send(self.room_group, {
                        'type': 'chat_message',
                        'sender': 'bot',
                        'text': '🔔 Un agent va vous rejoindre dans quelques instants. Temps d\'attente estimé : 2-5 min.',
                    })

        elif msg_type == 'request_human':
            await self.update_conv_status('pending')
            await self.channel_layer.group_send(self.room_group, {
                'type': 'chat_message',
                'sender': 'bot',
                'text': '🔔 Votre demande a été transmise à notre équipe. Un conseiller vous répond très bientôt !',
            })

    async def chat_message(self, event):
        await self.send(json.dumps({
            'type': 'message',
            'sender': event['sender'],
            'text': event['text'],
        }))

    # ─── Gemini ───────────────────────────────────────────────────────────────

    async def get_gemini_response(self, user_text):
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=SYSTEM_PROMPT
            )
            # Récupérer historique pour contexte
            history = await self.get_history()
            chat_history = []
            for m in history[-10:]:  # Max 10 derniers messages pour le contexte
                role = 'user' if m['sender'] == 'user' else 'model'
                chat_history.append({'role': role, 'parts': [m['text']]})

            chat = model.start_chat(history=chat_history)
            response = chat.send_message(user_text)
            return response.text
        except Exception as e:
            return f"Désolé, je rencontre un problème technique. Nos agents restent disponibles pour vous aider. ({str(e)[:50]})"

    # ─── DB helpers ───────────────────────────────────────────────────────────

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
        messages = Message.objects.filter(conversation=self.conversation).order_by('timestamp')
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
    def get_conv_status(self):
        self.conversation.refresh_from_db()
        return self.conversation.status

    @database_sync_to_async
    def update_conv_status(self, status):
        self.conversation.status = status
        self.conversation.save()