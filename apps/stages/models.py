from django.db import models
from django.contrib.auth.models import User


class DemandeStage(models.Model):

    TYPE_CHOICES = [
        ('vacances',         'Stage de vacances'),
        ('pre_emploi',       'Pré-emploi'),
        ('perfectionnement', 'Perfectionnement'),
    ]

    PROFIL_CHOICES = [
        ('eleve',               'Élève (Première / Terminale / Bac)'),
        ('etudiant',            'Étudiant (Validation BTS/HND)'),
        ('chomeur_travailleur', 'Chômeur / Travailleur'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_etude',   "En cours d'étude"),
        ('accepte',    'Accepté'),
        ('refuse',     'Refusé'),
    ]

    DOMAINE_CHOICES = [
        ('dev_web',    'Développement Web'),
        ('dev_mobile', 'Développement Mobile'),
        ('ia_data',    'IA & Data Science'),
        ('marketing',  'Marketing Digital'),
        ('design',     'Design UX/UI'),
        ('autre',      'Autre'),
    ]

    # Compte lié
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='demandes_stage', verbose_name='Compte'
    )

    # Informations personnelles
    nom           = models.CharField(max_length=100, verbose_name='Nom')
    prenom        = models.CharField(max_length=100, verbose_name='Prénom')
    telephone     = models.CharField(max_length=25, verbose_name='Téléphone')
    email_contact = models.EmailField(verbose_name='Email de contact')

    # Stage
    type_stage  = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=True, verbose_name='Type de stage')
    profil      = models.CharField(max_length=25, choices=PROFIL_CHOICES, verbose_name='Profil')
    domaine     = models.CharField(max_length=20, choices=DOMAINE_CHOICES, blank=True, verbose_name='Domaine souhaité')
    date_debut  = models.DateField(null=True, blank=True, verbose_name='Date de début souhaitée')
    date_fin    = models.DateField(null=True, blank=True, verbose_name='Date de fin souhaitée')

    # Documents communs
    lettre_motivation = models.TextField(verbose_name='Lettre de motivation')

    # Documents élève / étudiant
    certificat_scolarite  = models.FileField(upload_to='stages/docs/', blank=True, null=True, verbose_name='Certificat de scolarité (PDF)')
    lettre_responsable    = models.FileField(upload_to='stages/docs/', blank=True, null=True, verbose_name='Lettre du responsable (PDF)')
    carte_etudiant        = models.ImageField(upload_to='stages/docs/', blank=True, null=True, verbose_name='Carte étudiant')

    # Documents CNI (tous profils)
    cni_recto = models.ImageField(upload_to='stages/cni/', blank=True, null=True, verbose_name='CNI recto')
    cni_verso = models.ImageField(upload_to='stages/cni/', blank=True, null=True, verbose_name='CNI verso')

    # Documents chômeur / travailleur
    cv = models.FileField(upload_to='stages/cv/', blank=True, null=True, verbose_name='CV (PDF)')

    # Gestion admin
    statut            = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name='Statut')
    commentaire_admin = models.TextField(blank=True, verbose_name='Message pour le candidat')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de soumission')
    updated_at = models.DateTimeField(auto_now=True,     verbose_name='Dernière mise à jour')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Demande de stage'
        verbose_name_plural = 'Demandes de stage'

    def __str__(self):
        return f'{self.prenom} {self.nom} — {self.get_profil_display()} ({self.get_statut_display()})'
