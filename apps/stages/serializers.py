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
            username=email, email=email,
            password=validated_data['password'],
        )


# ── Demande ───────────────────────────────────────────────────────────────────

class DemandeStageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DemandeStage
        fields = [
            'nom', 'prenom', 'telephone', 'email_contact',
            'profil', 'domaine', 'date_debut', 'date_fin',
            'lettre_motivation',
            'certificat_scolarite', 'lettre_responsable', 'carte_etudiant',
            'cni_recto', 'cni_verso', 'cv',
        ]

    def validate(self, data):
        profil = data.get('profil')

        if profil == 'eleve':
            if not data.get('certificat_scolarite'):
                raise serializers.ValidationError(
                    {'certificat_scolarite': 'Le certificat de scolarité est obligatoire pour les élèves.'}
                )

        if profil == 'etudiant':
            if not data.get('certificat_scolarite'):
                raise serializers.ValidationError(
                    {'certificat_scolarite': 'Le certificat de scolarité est obligatoire pour les étudiants.'}
                )
            if not data.get('lettre_responsable'):
                raise serializers.ValidationError(
                    {'lettre_responsable': 'La lettre du responsable est obligatoire pour les étudiants.'}
                )

        if profil == 'chomeur_travailleur':
            if not data.get('cv'):
                raise serializers.ValidationError({'cv': 'Le CV est obligatoire.'})
            if not (data.get('cni_recto') and data.get('cni_verso')):
                raise serializers.ValidationError({'cni_recto': 'La CNI (recto et verso) est obligatoire.'})

        if data.get('date_debut') and data.get('date_fin'):
            if data['date_fin'] <= data['date_debut']:
                raise serializers.ValidationError({'date_fin': 'La date de fin doit être après la date de début.'})

        return data


class DemandeStageListSerializer(serializers.ModelSerializer):
    profil_display  = serializers.CharField(source='get_profil_display',    read_only=True)
    domaine_display = serializers.CharField(source='get_domaine_display',    read_only=True)
    statut_display  = serializers.CharField(source='get_statut_display',     read_only=True)

    class Meta:
        model  = DemandeStage
        fields = [
            'id', 'prenom', 'nom', 'email_contact',
            'profil', 'profil_display',
            'domaine', 'domaine_display',
            'date_debut', 'date_fin',
            'statut', 'statut_display',
            'commentaire_admin',
            'created_at', 'updated_at',
        ]


class DemandeStageDetailSerializer(DemandeStageListSerializer):
    class Meta(DemandeStageListSerializer.Meta):
        fields = DemandeStageListSerializer.Meta.fields + [
            'telephone', 'lettre_motivation',
            'certificat_scolarite', 'lettre_responsable', 'carte_etudiant',
            'cni_recto', 'cni_verso', 'cv',
        ]


class DecisionSerializer(serializers.Serializer):
    statut            = serializers.ChoiceField(choices=['accepte', 'refuse', 'en_etude'])
    commentaire_admin = serializers.CharField(allow_blank=True, default='')
