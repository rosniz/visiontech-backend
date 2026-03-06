# chat/models.py
import uuid
from django.db import models


class Conversation(models.Model):
    STATUS_CHOICES = [
        ('bot', 'Bot IA'),
        ('pending', 'En attente agent'),
        ('human', 'Agent humain'),
        ('closed', 'Fermé'),
    ]

    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='bot')
    visitor_name = models.CharField(max_length=100, blank=True, null=True)
    visitor_email = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_agent = models.ForeignKey(
        'auth.User', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='conversations'
    )

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conv {self.session_id} [{self.status}]"


class Message(models.Model):
    SENDER_CHOICES = [
        ('user', 'Utilisateur'),
        ('bot', 'Bot IA'),
        ('agent', 'Agent humain'),
    ]

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    content = models.TextField()
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.sender}] {self.content[:50]}"