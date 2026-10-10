from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contact
from .serializers import ContactSerializer
from .emails import send_contact_emails


class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les messages de contact
    
    Liste, créé, récupère, modifie et supprime les messages de contact
    """
    
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['lu']
    search_fields = ['nom', 'email', 'sujet', 'message']
    ordering_fields = ['date', 'nom']
    ordering = ['-date']

    def get_permissions(self):
        # Seul l'envoi d'un message est public ; la lecture et la gestion sont réservées aux admins
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        instance = serializer.save()
        try:
            send_contact_emails(instance)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f'Contact email failed: {e}')
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Marquer un message comme lu"""
        contact = self.get_object()
        contact.lu = True
        contact.save()
        return Response({
            'status': 'Message marqué comme lu',
            'lu': contact.lu
        })
    
    @action(detail=True, methods=['post'])
    def mark_as_unread(self, request, pk=None):
        """Marquer un message comme non lu"""
        contact = self.get_object()
        contact.lu = False
        contact.save()
        return Response({
            'status': 'Message marqué comme non lu',
            'lu': contact.lu
        })
