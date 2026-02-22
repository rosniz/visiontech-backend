from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les messages de contact
    
    Liste, créé, récupère, modifie et supprime les messages de contact
    """
    
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['lu']
    search_fields = ['nom', 'email', 'message']
    ordering_fields = ['date', 'nom']
    ordering = ['-date']
    
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
