from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import DemandeStage
from .serializers import (
    RegisterSerializer,
    DemandeStageCreateSerializer,
    DemandeStageListSerializer,
    DemandeStageDetailSerializer,
)
from .emails import send_confirmation_email


# ── Auth ──────────────────────────────────────────────────────────────────────

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user    = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
            'email':   user.email,
        }, status=status.HTTP_201_CREATED)


# ── Demandes ──────────────────────────────────────────────────────────────────

class MesDemandesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DemandeStageCreateSerializer
        return DemandeStageListSerializer

    def get_queryset(self):
        return DemandeStage.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        try:
            send_confirmation_email(instance)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f'Email confirmation failed: {e}')


class DemandeDetailView(generics.RetrieveAPIView):
    permission_classes  = [IsAuthenticated]
    serializer_class    = DemandeStageDetailSerializer

    def get_queryset(self):
        return DemandeStage.objects.filter(user=self.request.user)
