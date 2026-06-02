from django.contrib.auth.models import User
from rest_framework import serializers
from .models import DemandeStage


# ── Auth ──────────────────────────────────────────────────────────────────────

class RegisterSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    confirm  = serializers.CharField(write_only=True)

    def validate_email(self, value):
        v = value.lower().strip()
        if User.objects.filter(username=v).exists():
            raise serializers.ValidationError('Un compte avec cet email existe déjà.')
        return v

    def validate(self, data):
        if data['password'] != data['confirm']:
            raise serializers.ValidationError({'confirm': 'Les mots de passe ne correspondent pas.'})
        return data

    def create(self, validated_data):
        email = validated_data['email']
        return User.objects.create_user(
            username=email,
            email=email,
            password=validated_data['password'],
        )


# ── Demande ───────────────────────────────────────────────────────────────────

class DemandeStageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DemandeStage
        fields = [
            'nom', 'prenom', 'telephone', 'email_contact',
            'type_stage', 'domaine', 'date_debut', 'date_fin',
            'lettre_motivation',
            'cni_recto', 'cni_verso', 'carte_etudiant', 'certificat_scolarite',
            'cv',
        ]

    def validate(self, data):
        t = data.get('type_stage')

        if t == 'vacances':
            has_cni       = data.get('cni_recto') and data.get('cni_verso')
            has_etudiant  = data.get('carte_etudiant') and data.get('certificat_scolarite')
            if not has_cni and not has_etudiant:
                raise serializers.ValidationError(
                    'Pour un stage de vacances, fournissez CNI (recto+verso) OU carte étudiant + certificat de scolarité.'
                )

        if t in ('pre_emploi', 'perfectionnement'):
            if not data.get('cv'):
                raise serializers.ValidationError({'cv': 'Le CV est obligatoire.'})
            if not (data.get('cni_recto') and data.get('cni_verso')):
                raise serializers.ValidationError({'cni_recto': 'La CNI (recto et verso) est obligatoire.'})

        if data.get('date_debut') and data.get('date_fin'):
            if data['date_fin'] <= data['date_debut']:
                raise serializers.ValidationError({'date_fin': 'La date de fin doit être après la date de début.'})

        return data


class DemandeStageListSerializer(serializers.ModelSerializer):
    type_stage_display = serializers.CharField(source='get_type_stage_display', read_only=True)
    statut_display     = serializers.CharField(source='get_statut_display',     read_only=True)

    class Meta:
        model  = DemandeStage
        fields = [
            'id', 'type_stage', 'type_stage_display',
            'statut', 'statut_display',
            'commentaire_admin',
            'created_at', 'updated_at',
        ]


class DemandeStageDetailSerializer(serializers.ModelSerializer):
    type_stage_display = serializers.CharField(source='get_type_stage_display', read_only=True)
    domaine_display    = serializers.CharField(source='get_domaine_display',     read_only=True)
    statut_display     = serializers.CharField(source='get_statut_display',      read_only=True)

    class Meta:
        model  = DemandeStage
        exclude = ['user']
        read_only_fields = [f.name for f in DemandeStage._meta.get_fields() if hasattr(f, 'name')]
