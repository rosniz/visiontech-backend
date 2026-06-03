from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import DemandeStage
from .serializers import (
    RegisterSerializer,
    DemandeStageCreateSerializer,
    DemandeStageListSerializer,
    DemandeStageDetailSerializer,
    DecisionSerializer,
)
from .emails import send_confirmation_email, send_status_update_email
from rest_framework_simplejwt.tokens import RefreshToken


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


# ── Candidat ──────────────────────────────────────────────────────────────────

class MesDemandesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return DemandeStageCreateSerializer if self.request.method == 'POST' else DemandeStageListSerializer

    def get_queryset(self):
        return DemandeStage.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        try:
            send_confirmation_email(instance)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f'Email confirmation failed: {e}')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            DemandeStageListSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED
        )


class DemandeDetailView(generics.RetrieveAPIView):
    permission_classes  = [IsAuthenticated]
    serializer_class    = DemandeStageDetailSerializer

    def get_queryset(self):
        return DemandeStage.objects.filter(user=self.request.user)


# ── Admin ─────────────────────────────────────────────────────────────────────

class AdminDemandesListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class   = DemandeStageListSerializer
    queryset           = DemandeStage.objects.all()

    def get_queryset(self):
        qs     = super().get_queryset()
        statut = self.request.query_params.get('statut')
        profil = self.request.query_params.get('profil')
        if statut: qs = qs.filter(statut=statut)
        if profil: qs = qs.filter(profil=profil)
        return qs


class AdminDemandeDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    serializer_class   = DemandeStageDetailSerializer
    queryset           = DemandeStage.objects.all()


class AdminDecisionView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            demande = DemandeStage.objects.get(pk=pk)
        except DemandeStage.DoesNotExist:
            return Response({'error': 'Demande introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        demande.statut            = serializer.validated_data['statut']
        demande.commentaire_admin = serializer.validated_data['commentaire_admin']
        demande.save()

        try:
            send_status_update_email(demande)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f'Email status update failed: {e}')

        return Response(DemandeStageListSerializer(demande).data)


class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = DemandeStage.objects.all()
        return Response({
            'total':       qs.count(),
            'en_attente':  qs.filter(statut='en_attente').count(),
            'en_etude':    qs.filter(statut='en_etude').count(),
            'accepte':     qs.filter(statut='accepte').count(),
            'refuse':      qs.filter(statut='refuse').count(),
        })
