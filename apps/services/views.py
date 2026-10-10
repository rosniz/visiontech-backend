from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import IsAdminOrReadOnly
from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API simple pour gérer les services
    """

    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'description_courte', 'description']
    ordering_fields = ['created_at', 'nom', 'prix_a_partir_de', 'ordre']
    ordering = ['ordre', '-created_at']

    def get_queryset(self):
        # Les admins voient aussi les services désactivés
        if self.request.user.is_staff:
            return Service.objects.all()
        return Service.objects.filter(est_actif=True)
