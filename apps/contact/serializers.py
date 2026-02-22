from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Contact"""
    
    class Meta:
        model = Contact
        fields = [
            'id',
            'nom',
            'email',
            'message',
            'date',
            'lu'
        ]
        read_only_fields = ['id', 'date', 'lu']
    
    def validate_email(self, value):
        """Validation de l'email"""
        if not value:
            raise serializers.ValidationError("L'email est requis")
        return value.lower()
    
    def validate_message(self, value):
        """Validation du message"""
        if len(value) < 10:
            raise serializers.ValidationError(
                "Le message doit contenir au moins 10 caractères"
            )
        return value
