from rest_framework import viewsets
from core.permissions import IsAdminOrReadOnly
from .models import Formation
from .serializers import FormationListSerializer, FormationDetailSerializer

class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        # La liste reste légère ; le détail et l'écriture exposent tous les champs
        if self.action == 'list':
            return FormationListSerializer
        return FormationDetailSerializer
