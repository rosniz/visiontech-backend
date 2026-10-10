import logging

from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ParametresSite

security_log = logging.getLogger('security')


class ParametresSiteSerializer(serializers.ModelSerializer):
    updated_by_email = serializers.CharField(source='updated_by.email', read_only=True, default=None)

    class Meta:
        model  = ParametresSite
        fields = ['maintenance_active', 'maintenance_message', 'maintenance_fin', 'updated_at', 'updated_by_email']
        read_only_fields = ['updated_at', 'updated_by_email']


class StatutSiteView(APIView):
    """Public : le frontend l'interroge pour afficher (ou non) la page de maintenance."""
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response(ParametresSite.etat_maintenance())


class ParametresSiteAdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(ParametresSiteSerializer(ParametresSite.charger()).data)

    def patch(self, request):
        obj = ParametresSite.charger()
        avant = obj.maintenance_active
        serializer = ParametresSiteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        if avant != obj.maintenance_active:
            security_log.warning(
                'Mode maintenance %s par %s',
                'ACTIVÉ' if obj.maintenance_active else 'désactivé', request.user.email,
            )
        return Response(serializer.data)
