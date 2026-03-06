# ═══════════════════════════════════════════════════
# chat/admin.py
# ═══════════════════════════════════════════════════
from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['sender', 'content', 'timestamp']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'status', 'visitor_name', 'visitor_email', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['visitor_name', 'visitor_email', 'session_id']
    inlines = [MessageInline]
    readonly_fields = ['session_id', 'created_at', 'updated_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'content_preview', 'timestamp']
    list_filter = ['sender', 'timestamp']

    def content_preview(self, obj):
        return obj.content[:60]
    content_preview.short_description = 'Message'
