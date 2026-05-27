from rest_framework import serializers
from .models import Formation

class FormationListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des formations"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Formation
        fields = ['id', 'titre', 'sous_titre', 'description_courte', 'image_url', 'duree', 'niveau', 'prix']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class FormationDetailSerializer(serializers.ModelSerializer):
    """Serializer pour le détail d'une formation"""
    image_url = serializers.SerializerMethodField()
    syllabus_url = serializers.SerializerMethodField()

    class Meta:
        model = Formation
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_syllabus_url(self, obj):
        if obj.syllabus:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.syllabus.url) if request else obj.syllabus.url
        return None