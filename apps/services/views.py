from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API simple pour gérer les services
    """
    
    queryset = Service.objects.filter(est_actif=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'description_courte', 'description']
    ordering_fields = ['created_at', 'nom', 'prix_a_partir_de', 'ordre']
    ordering = ['ordre', '-created_at']