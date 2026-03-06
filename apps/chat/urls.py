
# ═══════════════════════════════════════════════════
# chat/urls.py
# ═══════════════════════════════════════════════════
from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_conversation, name='chat-start'),
    path('conversations/', views.list_conversations, name='chat-list'),
    path('conversations/<uuid:session_id>/', views.conversation_detail, name='chat-detail'),
    path('conversations/<uuid:session_id>/send/', views.agent_send_message, name='chat-agent-send'),
    path('stats/', views.chat_stats, name='chat-stats'),
]
