from decimal import Decimal

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CATEGORIE_CHOICES, Budget, Charge, FinanceProfile, TypeCharge
from .permissions import IsFinanceAdmin, IsFinanceUser
from .serializers import (
    BudgetSerializer,
    ChargeSerializer,
    FinanceUserCreateSerializer,
    FinanceUserSerializer,
    TypeChargeSerializer,
)


def _add_months(year, month, offset):
    total = (year * 12 + (month - 1)) + offset
    return total // 12, total % 12 + 1


# ── Charges / Types / Budgets ────────────────────────────────────────────────

class ChargeViewSet(viewsets.ModelViewSet):
    queryset = Charge.objects.select_related('type_charge', 'created_by').all()
    serializer_class = ChargeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categorie', 'type_charge', 'statut', 'mode_paiement']
    search_fields = ['libelle', 'beneficiaire', 'reference_piece']
    ordering_fields = ['date_charge', 'montant', 'created_at']
    ordering = ['-date_charge']

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsFinanceAdmin()]
        return [IsFinanceUser()]

    def get_queryset(self):
        qs = super().get_queryset()
        date_debut = self.request.query_params.get('date_debut')
        date_fin = self.request.query_params.get('date_fin')
        if date_debut:
            qs = qs.filter(date_charge__gte=date_debut)
        if date_fin:
            qs = qs.filter(date_charge__lte=date_fin)
        return qs


class TypeChargeViewSet(viewsets.ModelViewSet):
    queryset = TypeCharge.objects.all()
    serializer_class = TypeChargeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categorie', 'actif']
    search_fields = ['nom', 'description']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsFinanceUser()]
        return [IsFinanceAdmin()]


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.select_related('created_by').all()
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categorie', 'annee', 'mois']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsFinanceUser()]
        return [IsFinanceAdmin()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ── Dashboard ─────────────────────────────────────────────────────────────────

class DashboardRepartitionView(APIView):
    permission_classes = [IsFinanceUser]

    def get(self, request):
        today = timezone.now().date()
        annee = int(request.query_params.get('annee', today.year))
        mois = request.query_params.get('mois')

        qs = Charge.objects.filter(date_charge__year=annee)
        if mois:
            qs = qs.filter(date_charge__month=int(mois))

        totals = {
            row['categorie']: row
            for row in qs.values('categorie').annotate(total=Sum('montant'), nombre=Count('id'))
        }

        repartition = [
            {
                'categorie': code,
                'categorie_display': label,
                'total': totals.get(code, {}).get('total') or Decimal('0'),
                'nombre': totals.get(code, {}).get('nombre') or 0,
            }
            for code, label in CATEGORIE_CHOICES
        ]

        return Response({
            'annee': annee,
            'mois': int(mois) if mois else None,
            'repartition': repartition,
        })


class DashboardEvolutionView(APIView):
    permission_classes = [IsFinanceUser]

    def get(self, request):
        try:
            nb_mois = max(1, min(36, int(request.query_params.get('mois', 12))))
        except ValueError:
            nb_mois = 12

        today = timezone.now().date()
        start_year, start_month = _add_months(today.year, today.month, -(nb_mois - 1))
        start = today.replace(year=start_year, month=start_month, day=1)

        rows = (
            Charge.objects.filter(date_charge__gte=start)
            .annotate(month=TruncMonth('date_charge'))
            .values('month', 'categorie')
            .annotate(total=Sum('montant'))
            .order_by('month')
        )

        pivot = {}
        for row in rows:
            key = row['month'].strftime('%Y-%m')
            pivot.setdefault(key, {code: Decimal('0') for code, _ in CATEGORIE_CHOICES})
            pivot[key][row['categorie']] = row['total']

        evolution = []
        year, month = start_year, start_month
        for _ in range(nb_mois):
            key = f'{year:04d}-{month:02d}'
            valeurs = pivot.get(key, {code: Decimal('0') for code, _ in CATEGORIE_CHOICES})
            evolution.append({'mois': key, **valeurs, 'total': sum(valeurs.values())})
            year, month = _add_months(year, month, 1)

        return Response({'evolution': evolution})


class DashboardBudgetsView(APIView):
    permission_classes = [IsFinanceUser]

    def get(self, request):
        today = timezone.now().date()
        annee = int(request.query_params.get('annee', today.year))
        mois = int(request.query_params.get('mois', today.month))

        actuals = {
            row['categorie']: row['total']
            for row in Charge.objects.filter(date_charge__year=annee, date_charge__month=mois)
            .values('categorie').annotate(total=Sum('montant'))
        }

        comparatif = []
        alertes = []
        for budget in Budget.objects.filter(annee=annee, mois=mois):
            actual = actuals.get(budget.categorie) or Decimal('0')
            if budget.montant_prevu:
                pourcentage = float(actual / budget.montant_prevu * 100)
            else:
                pourcentage = 100.0 if actual else 0.0

            if pourcentage >= 100:
                statut = 'depassement'
            elif pourcentage >= budget.seuil_alerte:
                statut = 'attention'
            else:
                statut = 'ok'

            item = {
                'categorie': budget.categorie,
                'categorie_display': budget.get_categorie_display(),
                'montant_prevu': budget.montant_prevu,
                'montant_reel': actual,
                'ecart': actual - budget.montant_prevu,
                'pourcentage': round(pourcentage, 1),
                'seuil_alerte': budget.seuil_alerte,
                'statut': statut,
            }
            comparatif.append(item)
            if statut != 'ok':
                alertes.append(item)

        return Response({'annee': annee, 'mois': mois, 'comparatif': comparatif, 'alertes': alertes})


class DashboardComparatifView(APIView):
    permission_classes = [IsFinanceUser]

    def get(self, request):
        p1 = self._parse_periode(request.query_params.get('periode1'))
        p2 = self._parse_periode(request.query_params.get('periode2'))
        if not p1 or not p2:
            return Response(
                {'detail': "Paramètres 'periode1' et 'periode2' requis, format AAAA-MM."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        def totals_for(periode):
            annee, mois = periode
            rows = (
                Charge.objects.filter(date_charge__year=annee, date_charge__month=mois)
                .values('categorie').annotate(total=Sum('montant'))
            )
            data = {row['categorie']: row['total'] for row in rows}
            return {code: data.get(code) or Decimal('0') for code, _ in CATEGORIE_CHOICES}

        totaux1 = totals_for(p1)
        totaux2 = totals_for(p2)

        comparaison = []
        for code, label in CATEGORIE_CHOICES:
            v1, v2 = totaux1[code], totaux2[code]
            variation_pct = round(float((v2 - v1) / v1 * 100), 1) if v1 else None
            comparaison.append({
                'categorie': code,
                'categorie_display': label,
                'periode1': v1,
                'periode2': v2,
                'variation': v2 - v1,
                'variation_pct': variation_pct,
            })

        return Response({
            'periode1': f'{p1[0]}-{p1[1]:02d}',
            'periode2': f'{p2[0]}-{p2[1]:02d}',
            'comparaison': comparaison,
        })

    @staticmethod
    def _parse_periode(value):
        if not value:
            return None
        try:
            annee, mois = value.split('-')
            return int(annee), int(mois)
        except (ValueError, AttributeError):
            return None


# ── Gestion des utilisateurs finance ─────────────────────────────────────────

class FinanceUsersView(generics.ListCreateAPIView):
    permission_classes = [IsFinanceAdmin]
    queryset = FinanceProfile.objects.select_related('user').all()

    def get_serializer_class(self):
        return FinanceUserCreateSerializer if self.request.method == 'POST' else FinanceUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response(FinanceUserSerializer(profile).data, status=status.HTTP_201_CREATED)


class FinanceUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsFinanceAdmin]
    queryset = FinanceProfile.objects.select_related('user').all()
    serializer_class = FinanceUserSerializer
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']
