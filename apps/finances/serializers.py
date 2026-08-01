from django.contrib.auth.models import User
from rest_framework import serializers

from .models import ROLE_CHOICES, Budget, Charge, FinanceProfile, TypeCharge


class TypeChargeSerializer(serializers.ModelSerializer):
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)

    class Meta:
        model = TypeCharge
        fields = ['id', 'categorie', 'categorie_display', 'nom', 'description', 'actif', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ChargeSerializer(serializers.ModelSerializer):
    categorie = serializers.CharField(read_only=True)
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)
    type_charge_nom = serializers.CharField(source='type_charge.nom', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    mode_paiement_display = serializers.CharField(source='get_mode_paiement_display', read_only=True)
    justificatif_url = serializers.SerializerMethodField()
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)

    class Meta:
        model = Charge
        fields = [
            'id', 'categorie', 'categorie_display', 'type_charge', 'type_charge_nom',
            'libelle', 'montant', 'date_charge', 'beneficiaire', 'reference_piece',
            'mode_paiement', 'mode_paiement_display', 'statut', 'statut_display',
            'justificatif', 'justificatif_url', 'details', 'notes',
            'created_by', 'created_by_email', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_justificatif_url(self, obj):
        if obj.justificatif:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.justificatif.url) if request else obj.justificatif.url
        return None

    def create(self, validated_data):
        validated_data['categorie'] = validated_data['type_charge'].categorie
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'type_charge' in validated_data:
            validated_data['categorie'] = validated_data['type_charge'].categorie
        return super().update(instance, validated_data)


class BudgetSerializer(serializers.ModelSerializer):
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)

    class Meta:
        model = Budget
        fields = [
            'id', 'categorie', 'categorie_display', 'annee', 'mois', 'montant_prevu',
            'seuil_alerte', 'notes', 'created_by', 'created_by_email', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class FinanceUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = FinanceProfile
        fields = ['id', 'user', 'email', 'username', 'role', 'role_display', 'actif', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


class FinanceUserCreateSerializer(serializers.Serializer):
    """Attribue un rôle finance à un utilisateur Django existant, identifié par email."""

    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email__iexact=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Aucun utilisateur avec cet email. Créez d'abord son compte (ex: via l'admin Django) "
                "avant de lui attribuer un rôle finance."
            )
        return value

    def save(self, **kwargs):
        profile, _ = FinanceProfile.objects.update_or_create(
            user=self.user,
            defaults={'role': self.validated_data['role'], 'actif': True},
        )
        return profile
