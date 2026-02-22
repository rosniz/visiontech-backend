from rest_framework import serializers
from .models import Formation

class FormationListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des formations"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Formation
        fields = ['id', 'titre', 'sous_titre', 'description_courte', 'image_url', 'duree', 'niveau', 'prix']
    
    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class FormationDetailSerializer(serializers.ModelSerializer):
    """Serializer pour le détail d'une formation"""
    image_url = serializers.SerializerMethodField()
    syllabus_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Formation
        fields = '__all__'
    
    def get_image_url(self, obj):
        return obj.image.url if obj.image else None
    
    def get_syllabus_url(self, obj):
        return obj.syllabus.url if obj.syllabus else None