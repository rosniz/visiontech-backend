from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Formation
from .serializers import FormationListSerializer, FormationDetailSerializer

class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FormationDetailSerializer
        return FormationListSerializer