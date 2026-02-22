from rest_framework import serializers
from .models import Realisation


class RealisationSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Realisation"""

    image_url = serializers.SerializerMethodField()
    technologies_list = serializers.SerializerMethodField()
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)

    class Meta:
        model = Realisation
        fields = [
            'id',
            'titre',
            'description',
            'image',
            'image_url',
            'lien',
            'categorie',
            'categorie_display',
            'client',
            'technologies',
            'technologies_list',
            'statut',
            'statut_display',
            'ordre',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


    def get_image_url(self, obj):
        """Retourne l'URL complète de l'image Cloudinary"""
        if obj.image:
            return obj.image.url
        return None

    def get_technologies_list(self, obj):
        """Retourne les technologies sous forme de liste"""
        if obj.technologies:
            return [tech.strip() for tech in obj.technologies.split(',')]
        return []