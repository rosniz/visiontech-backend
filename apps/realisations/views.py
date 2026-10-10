from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import IsAdminOrReadOnly
from .models import Realisation
from .serializers import RealisationSerializer


class RealisationViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les réalisations

    Liste, créé, récupère, modifie et supprime les réalisations
    """

    queryset = Realisation.objects.all()
    serializer_class = RealisationSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'client','categorie']
    search_fields = ['titre', 'description', 'client', 'technologies']
    ordering_fields = ['ordre', 'created_at', 'titre']
    ordering = ['ordre', '-created_at']