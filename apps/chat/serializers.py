# ═══════════════════════════════════════════════════
# chat/serializers.py
# ═══════════════════════════════════════════════════
from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'timestamp', 'is_read']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'session_id', 'status', 'visitor_name',
            'visitor_email', 'created_at', 'updated_at',
            'message_count', 'last_message', 'messages'
        ]

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_last_message(self, obj):
        last = obj.messages.last()
        return last.content[:80] if last else None

