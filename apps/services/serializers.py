from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Service"""
    
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id',
            'nom',
            'description_courte',
            'description',
            'image',
            'image_url',
            'points_forts',
            'prix_a_partir_de',
            'duree_estimee',
            'est_actif',
            'ordre',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_image_url(self, obj):
        """Retourne l'URL de l'image Cloudinary"""
        if obj.image:
            return obj.image.url
        return None
    
    def to_representation(self, instance):
        """Personnaliser la représentation pour s'assurer que points_forts est un array"""
        representation = super().to_representation(instance)
        
        # S'assurer que points_forts est toujours un array
        if representation.get('points_forts') is None:
            representation['points_forts'] = []
        elif isinstance(representation['points_forts'], str):
            # Si c'est une string, essayer de la parser
            try:
                import json
                representation['points_forts'] = json.loads(representation['points_forts'])
            except:
                representation['points_forts'] = []
        
        return representation


class ServiceListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des services"""
    
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id',
            'nom',
            'description_courte',
            'image_url',
            'prix_a_partir_de',
            'duree_estimee',
            'est_actif',
            'ordre'
        ]
    
    def get_image_url(self, obj):
        """Retourne l'URL de l'image Cloudinary"""
        if obj.image:
            return obj.image.url
        return None


class ServiceDetailSerializer(ServiceSerializer):
    """Serializer détaillé pour un service (hérite de ServiceSerializer)"""
    pass