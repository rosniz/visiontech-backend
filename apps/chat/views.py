# ═══════════════════════════════════════════════════
# chat/views.py
# ═══════════════════════════════════════════════════
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
import uuid


@api_view(['POST'])
@permission_classes([AllowAny])
def start_conversation(request):
    """Crée ou récupère une session de chat."""
    session_id = request.data.get('session_id') or str(uuid.uuid4())
    conv, created = Conversation.objects.get_or_create(session_id=session_id)
    if 'visitor_name' in request.data:
        conv.visitor_name = request.data['visitor_name']
        conv.save()
    return Response({
        'session_id': str(conv.session_id),
        'status': conv.status,
        'created': created
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_conversations(request):
    """Liste toutes les conversations (admin/agent)."""
    status_filter = request.query_params.get('status')
    convs = Conversation.objects.all()
    if status_filter:
        convs = convs.filter(status=status_filter)
    serializer = ConversationSerializer(convs, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def conversation_detail(request, session_id):
    """Détail d'une conversation + changement de statut."""
    try:
        conv = Conversation.objects.get(session_id=session_id)
    except Conversation.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        serializer = ConversationSerializer(conv)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        new_status = request.data.get('status')
        if new_status in dict(Conversation.STATUS_CHOICES):
            conv.status = new_status
            conv.save()
        return Response(ConversationSerializer(conv).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agent_send_message(request, session_id):
    """Permet à un agent humain d'envoyer un message."""
    try:
        conv = Conversation.objects.get(session_id=session_id)
    except Conversation.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    content = request.data.get('content', '').strip()
    if not content:
        return Response({'error': 'Message vide'}, status=400)

    msg = Message.objects.create(conversation=conv, content=content, sender='agent')

    # Mettre à jour le statut si nécessaire
    if conv.status != 'human':
        conv.status = 'human'
        conv.assigned_agent = request.user
        conv.save()

    return Response(MessageSerializer(msg).data, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_stats(request):
    """Statistiques pour le dashboard agent."""
    return Response({
        'total': Conversation.objects.count(),
        'bot': Conversation.objects.filter(status='bot').count(),
        'pending': Conversation.objects.filter(status='pending').count(),
        'human': Conversation.objects.filter(status='human').count(),
        'closed': Conversation.objects.filter(status='closed').count(),
    })
