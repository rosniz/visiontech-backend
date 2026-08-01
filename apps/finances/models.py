from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

CATEGORIE_EXPLOITATION = 'exploitation'
CATEGORIE_FISCALE = 'fiscale'
CATEGORIE_PERSONNEL = 'personnel'
CATEGORIE_FINANCIERE = 'financiere'

CATEGORIE_CHOICES = [
    (CATEGORIE_EXPLOITATION, "Charges d'exploitation"),
    (CATEGORIE_FISCALE, 'Charges fiscales'),
    (CATEGORIE_PERSONNEL, 'Charges de personnel'),
    (CATEGORIE_FINANCIERE, 'Charges financières'),
]

ROLE_ADMIN = 'admin'
ROLE_COMPTABLE = 'comptable'

ROLE_CHOICES = [
    (ROLE_ADMIN, 'Administrateur'),
    (ROLE_COMPTABLE, 'Comptable'),
]


class FinanceProfile(models.Model):
    """Habilitation d'un utilisateur sur le module finances (indépendante de is_staff)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='finance_profile', verbose_name='Utilisateur'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_COMPTABLE, verbose_name='Rôle')
    actif = models.BooleanField(default=True, verbose_name='Accès actif')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__email']
        verbose_name = 'Profil finance'
        verbose_name_plural = 'Profils finance'

    def __str__(self):
        return f'{self.user.email} ({self.get_role_display()})'


class TypeCharge(models.Model):
    """Sous-catégorie d'une charge (ex: sous 'fiscale' -> IS, TVA, taxe foncière)."""

    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, db_index=True, verbose_name='Catégorie')
    nom = models.CharField(max_length=150, verbose_name='Nom du type')
    description = models.TextField(blank=True, verbose_name='Description')
    actif = models.BooleanField(default=True, verbose_name='Actif')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['categorie', 'nom']
        unique_together = ('categorie', 'nom')
        verbose_name = 'Type de charge'
        verbose_name_plural = 'Types de charge'

    def __str__(self):
        return f'{self.nom} ({self.get_categorie_display()})'


class Charge(models.Model):
    """Une charge d'entreprise, quelle que soit sa catégorie."""

    MODE_PAIEMENT_CHOICES = [
        ('virement', 'Virement bancaire'),
        ('especes', 'Espèces'),
        ('cheque', 'Chèque'),
        ('mobile_money', 'Mobile Money'),
        ('autre', 'Autre'),
    ]

    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('validee', 'Validée'),
        ('payee', 'Payée'),
    ]

    # Dénormalisé depuis type_charge.categorie (synchronisé côté serializer) pour
    # permettre le filtrage/l'agrégation du dashboard sans jointure.
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, db_index=True, verbose_name='Catégorie')
    type_charge = models.ForeignKey(
        TypeCharge, on_delete=models.PROTECT, related_name='charges', verbose_name='Type de charge'
    )

    libelle = models.CharField(max_length=255, verbose_name='Libellé')
    montant = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Montant (FCFA)'
    )
    date_charge = models.DateField(db_index=True, verbose_name='Date de la charge')

    beneficiaire = models.CharField(
        max_length=200, blank=True, verbose_name='Bénéficiaire',
        help_text='Fournisseur, employé, banque...'
    )
    reference_piece = models.CharField(max_length=100, blank=True, verbose_name='Référence pièce justificative')
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES, blank=True, verbose_name='Mode de paiement')
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='validee', verbose_name='Statut')

    justificatif = models.FileField(upload_to='finances/justificatifs/%Y/%m/', blank=True, null=True, verbose_name='Pièce justificative')
    details = models.JSONField(
        default=dict, blank=True, verbose_name='Détails spécifiques',
        help_text="Champs propres à la catégorie (ex: taux d'intérêt, matricule employé...)"
    )
    notes = models.TextField(blank=True, verbose_name='Notes')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='charges_creees', verbose_name='Créée par'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_charge']
        verbose_name = 'Charge'
        verbose_name_plural = 'Charges'
        indexes = [
            models.Index(fields=['categorie', 'date_charge']),
        ]

    def __str__(self):
        return f'{self.libelle} — {self.montant} FCFA ({self.date_charge})'


class Budget(models.Model):
    """Budget prévisionnel mensuel par catégorie, utilisé pour les alertes de dépassement."""

    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, verbose_name='Catégorie')
    annee = models.IntegerField(validators=[MinValueValidator(2020)], verbose_name='Année')
    mois = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], verbose_name='Mois')
    montant_prevu = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Montant prévu (FCFA)'
    )
    seuil_alerte = models.IntegerField(
        default=90, validators=[MinValueValidator(1), MaxValueValidator(150)],
        verbose_name="Seuil d'alerte (%)"
    )
    notes = models.TextField(blank=True, verbose_name='Notes')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='budgets_crees', verbose_name='Créé par'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-annee', '-mois', 'categorie']
        unique_together = ('categorie', 'annee', 'mois')
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'

    def __str__(self):
        return f'{self.get_categorie_display()} {self.mois}/{self.annee} — {self.montant_prevu} FCFA'
