# chat/consumers.py
import json
import re
import google.generativeai as genai
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message

WHATSAPP_NUMBER = '237674554947'

# ─── Mots-clés pour détecter quel type de données chercher ────────────────────
DB_KEYWORDS = {
    'formations': [
        'formation', 'formations', 'cours', 'apprendre', 'programme', 'syllabus',
        'certif', 'learn', 'training', 'étudier', 'niveau', 'durée',
        'python', 'javascript', 'react', 'django', 'machine learning',
        'deep learning', 'ia', 'intelligence artificielle', 'data',
        'quelles formations', 'vos formations', 'avez-vous des formations',
        'proposez-vous', 'offrez-vous', 'formation disponible',
    ],
    'services': [
        'service', 'services', 'offre', 'solution', 'prestation', 'développer',
        'chatbot', 'automatisation', 'vision', 'reconnaissance', 'prédictif',
        'intégration', 'consulting', 'audit', 'conseil', 'tarif', 'prix',
        'combien', 'coût', 'budget', 'forfait', 'vos services', 'que faites',
        'que proposez', 'spécialité', 'expertise',
    ],
    'realisations': [
        'réalisation', 'réalisations', 'projet', 'projets', 'portfolio',
        'client', 'exemple', 'référence', 'travail', 'réalisé', 'fait',
        'technologie', 'réussi', 'success', 'case study', 'achievement',
        'avez-vous déjà', 'avez vous fait', 'montrez', 'exemples',
    ],
}

SYSTEM_PROMPT = """Tu es l'assistant virtuel de VisionTech SARL, une entreprise basée à Bafoussam, Cameroun.

VisionTech SARL propose :
1. Des FORMATIONS en IA et technologie (voir données [DONNÉES] pour les détails exacts)
2. Des SERVICES de conception IA sur-mesure (chatbots, vision par ordinateur, automatisation, ML)
3. Des RÉALISATIONS/PROJETS clients (voir données [DONNÉES] pour les exemples)

Localisation : Bafoussam, Région de l'Ouest, Cameroun.
Contact WhatsApp : +237 674 55 49 47

RÈGLES ABSOLUES :
1. Réponds dans la langue de l'utilisateur (français ou anglais)
2. Quand des données [DONNÉES] sont fournies, utilise-les DIRECTEMENT pour répondre — cite les vrais titres, prix, durées
3. Si aucune donnée n'est fournie pour une question précise, dis honnêtement que tu n'as pas l'info et propose de contacter l'équipe
4. Ne dis JAMAIS que VisionTech ne propose pas de formations — nous en proposons
5. Si la demande nécessite un devis ou une démo, dis exactement : "Je vais vous mettre en contact avec un de nos conseillers."
6. Sois concis : 3-4 phrases max
7. Prix toujours en FCFA"""

TRANSFER_KEYWORDS = [
    'humain', 'agent', 'conseiller', 'parler à quelqu\'un',
    'urgence', 'problème grave', 'rappel', 'devis',
    'démo', 'demonstration', 'rendez-vous', 'rdv', 'rencontre', 'appel'
]


def build_whatsapp_url(phone_number, conv_summary):
    msg = (
        f"Bonjour VisionTech 👋\n"
        f"Je vous contacte depuis le chat de votre site.\n\n"
        f"📋 Résumé de ma demande :\n{conv_summary}\n\n"
        f"Mon numéro : {phone_number}"
    )
    encoded = msg.replace(' ', '%20').replace('\n', '%0A')
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"


def detect_needed_data(text):
    """Détecte quels types de données chercher selon le message."""
    import unicodedata

    def normalize(s):
        # Supprime les accents pour comparer sans accent
        return ''.join(
            c for c in unicodedata.normalize('NFD', s.lower())
            if unicodedata.category(c) != 'Mn'
        )

    text_norm = normalize(text)
    needed = set()

    for data_type, keywords in DB_KEYWORDS.items():
        for kw in keywords:
            if normalize(kw) in text_norm:
                needed.add(data_type)
                break

    # Si le message est une question générale sur VisionTech, tout charger
    general_keywords = ['que proposez', 'que faites', 'votre offre', 'vos offres',
                        'what do you', 'what can you', 'tout', 'toutes']
    if any(normalize(kw) in text_norm for kw in general_keywords):
        needed = {'formations', 'services', 'realisations'}

    return needed


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group = f'chat_{self.session_id}'
        self.waiting_for_phone = False

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

            # ── Collecte du numéro WhatsApp ───────────────────────────────────
            if self.waiting_for_phone:
                phone = self.extract_phone(user_text)
                if phone:
                    self.waiting_for_phone = False
                    await self.update_visitor_phone(phone)
                    await self.update_conv_status('pending')
                    summary = await self.get_conv_summary()
                    wa_url = build_whatsapp_url(phone, summary)
                    wa_msg = f"WHATSAPP_CARD::{wa_url}::{phone}"
                    await self.save_message(wa_msg, 'bot')
                    await self.send(json.dumps({
                        'type': 'whatsapp_card',
                        'wa_url': wa_url,
                        'phone': phone,
                    }))
                else:
                    reply = "Je n'ai pas reconnu ce numéro. Merci d'entrer votre numéro WhatsApp avec l'indicatif (ex: 237 6XX XX XX XX)."
                    await self.save_message(reply, 'bot')
                    await self.broadcast('bot', reply)
                return

            # ── Mode bot avec RAG ─────────────────────────────────────────────
            if conv_status == 'bot':
                needs_transfer = any(kw in user_text.lower() for kw in TRANSFER_KEYWORDS)

                # Détecter les données nécessaires et les récupérer
                needed = detect_needed_data(user_text)
                db_context = await self.fetch_db_context(needed)

                # Générer la réponse avec contexte BD
                reply = await self.get_gemini_response(user_text, db_context)
                await self.save_message(reply, 'bot')
                await self.broadcast('bot', reply)

                if needs_transfer or 'conseillers' in reply.lower():
                    await self.trigger_whatsapp_flow()

        elif msg_type == 'request_human':
            await self.trigger_whatsapp_flow()

    # ── Flux WhatsApp ──────────────────────────────────────────────────────────
    async def trigger_whatsapp_flow(self):
        self.waiting_for_phone = True
        ask_msg = (
            "📱 Pour vous mettre en contact avec un conseiller VisionTech, "
            "merci de nous indiquer votre numéro WhatsApp "
            "(avec indicatif pays, ex: 237 674 55 49 47) :"
        )
        await self.save_message(ask_msg, 'bot')
        await self.broadcast('bot', ask_msg)

    async def broadcast(self, sender, text):
        await self.channel_layer.group_send(self.room_group, {
            'type': 'chat_message', 'sender': sender, 'text': text,
        })

    async def chat_message(self, event):
        await self.send(json.dumps({
            'type': 'message',
            'sender': event['sender'],
            'text': event['text'],
        }))

    # ── Récupération des données BD ───────────────────────────────────────────
    @database_sync_to_async
    def fetch_db_context(self, needed):
        """Récupère les données pertinentes depuis la BD et les formate."""
        if not needed:
            return ""

        context_parts = []

        if 'formations' in needed:
            try:
                # Essaie les deux chemins possibles
                try:
                    from apps.formations.models import Formation
                except ImportError:
                    from formations.models import Formation
                formations = list(Formation.objects.all()[:10])
                import logging
                logging.getLogger(__name__).info(f"[RAG] {len(formations)} formation(s) trouvée(s)")
                if formations:
                    lines = ["📚 FORMATIONS DISPONIBLES :"]
                    for f in formations:
                        line = f"• {f.titre}"
                        if f.sous_titre:
                            line += f" — {f.sous_titre}"
                        if f.niveau:
                            line += f" | Niveau : {f.niveau}"
                        if f.duree:
                            line += f" | Durée : {f.duree}"
                        if f.prix:
                            line += f" | Prix : {int(f.prix):,} FCFA"
                        else:
                            line += " | Prix : nous contacter"
                        if f.description_courte:
                            line += f"\n  → {f.description_courte}"
                        lines.append(line)
                    context_parts.append('\n'.join(lines))
                else:
                    logging.getLogger(__name__).warning("[RAG] Aucune formation en BD")
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"[RAG] Erreur formations: {e}")

        if 'services' in needed:
            try:
                try:
                    from apps.services.models import Service
                except ImportError:
                    from services.models import Service
                services = Service.objects.filter(est_actif=True).order_by('ordre')[:8]
                if services:
                    lines = ["🛠️ NOS SERVICES IA :"]
                    for s in services:
                        line = f"• {s.nom} — {s.description_courte}"
                        if s.prix_a_partir_de:
                            line += f" | À partir de {int(s.prix_a_partir_de):,} FCFA"
                        if s.duree_estimee:
                            line += f" | Durée : {s.duree_estimee}"
                        if s.points_forts:
                            points = ', '.join(s.points_forts[:3]) if isinstance(s.points_forts, list) else str(s.points_forts)
                            line += f"\n  → Points forts : {points}"
                        lines.append(line)
                    context_parts.append('\n'.join(lines))
            except Exception:
                pass

        if 'realisations' in needed:
            try:
                try:
                    from apps.realisations.models import Realisation
                except ImportError:
                    from realisations.models import Realisation
                reals = Realisation.objects.filter(statut='termine').order_by('ordre')[:6]
                if reals:
                    lines = ["🏆 NOS RÉALISATIONS :"]
                    for r in reals:
                        line = f"• {r.titre}"
                        if r.client:
                            line += f" (Client : {r.client})"
                        line += f" — Catégorie : {r.get_categorie_display()}"
                        if r.technologies:
                            line += f" | Technologies : {r.technologies}"
                        if r.description:
                            line += f"\n  → {r.description[:150]}..."
                        lines.append(line)
                    context_parts.append('\n'.join(lines))
            except Exception:
                pass

        return '\n\n'.join(context_parts)

    # ── Gemini avec contexte BD ───────────────────────────────────────────────
    async def get_gemini_response(self, user_text, db_context=''):
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=SYSTEM_PROMPT
            )

            history = await self.get_history()
            chat_history = []
            for m in history[-8:]:
                role = 'user' if m['sender'] == 'user' else 'model'
                chat_history.append({'role': role, 'parts': [m['text']]})

            # Construire le message avec contexte BD si disponible
            if db_context:
                enriched = (
                    f"[DONNÉES DE LA BASE — utilise ces infos pour répondre]\n"
                    f"{db_context}\n"
                    f"[FIN DES DONNÉES]\n\n"
                    f"Question de l'utilisateur : {user_text}"
                )
            else:
                enriched = user_text

            chat = model.start_chat(history=chat_history)
            response = chat.send_message(enriched)
            return response.text

        except Exception as e:
            return f"Désolé, je rencontre un problème technique. ({str(e)[:60]})"

    # ── Extraction numéro ──────────────────────────────────────────────────────
    def extract_phone(self, text):
        cleaned = re.sub(r'[\s\-\.\(\)]', '', text)
        patterns = [
            r'(\+?237[0-9]{8,9})',
            r'(\+?[0-9]{10,13})',
        ]
        for pattern in patterns:
            match = re.search(pattern, cleaned)
            if match:
                return re.sub(r'\+', '', match.group(1))
        return None

    # ── DB helpers ────────────────────────────────────────────────────────────
    @database_sync_to_async
    def get_or_create_conversation(self):
        conv, _ = Conversation.objects.get_or_create(session_id=self.session_id)
        return conv

    @database_sync_to_async
    def save_message(self, content, sender):
        return Message.objects.create(
            conversation=self.conversation, content=content, sender=sender
        )

    @database_sync_to_async
    def get_history(self):
        messages = Message.objects.filter(
            conversation=self.conversation
        ).order_by('timestamp')
        return [
            {'id': str(m.id), 'sender': m.sender, 'text': m.content, 'timestamp': m.timestamp.isoformat()}
            for m in messages
        ]

    @database_sync_to_async
    def get_conv_summary(self):
        messages = Message.objects.filter(
            conversation=self.conversation, sender='user'
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
        self.conversation.visitor_email = phone
        self.conversation.save()