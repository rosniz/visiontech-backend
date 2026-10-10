from django.db import models

from core.images import compresser_image


class Realisation(models.Model):
    """Modèle pour les réalisations de VisionTech"""

    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    ]

    CATEGORIE_CHOICES = [
    ('developpement', 'Développement Web'),
    ('mobile', 'Application Mobile'),
    ('formation', 'Formation & Atelier'),
    ('conseil', 'Conseil & Stratégie'),
    ('automatisation','IA & Automatisation')
    ]


    categorie = models.CharField(
    max_length=50,
    choices=CATEGORIE_CHOICES,
    default='developpement',
    verbose_name="Catégorie"
    )
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to='realisations/', blank=True, null=True)
    lien = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Lien",
        help_text="Lien vers le projet (optionnel)"
    )

    # Nouveaux champs
    client = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Client",
        help_text="Nom de l'entreprise cliente"
    )
    technologies = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Technologies utilisées",
        help_text="Ex: React, Django, PostgreSQL"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='termine',
        verbose_name="Statut"
    )
    ordre = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Priorité d'affichage (0 = le plus prioritaire)"
    )

    # Mise en avant dans le Hero de la page d'accueil
    en_vedette = models.BooleanField(
        default=False,
        verbose_name="Afficher dans le Hero de l'accueil",
        help_text="La réalisation défile dans le showcase en haut de la page d'accueil (ordre d'affichage respecté)"
    )
    accroche = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Accroche",
        help_text="Phrase courte affichée sous l'image dans le Hero"
    )
    logo = models.ImageField(
        upload_to='realisations/logos/',
        blank=True,
        null=True,
        verbose_name="Logo",
        help_text="Logo carré du produit (onglets du Hero)"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        ordering = ['ordre', '-created_at']
        verbose_name = "Réalisation"
        verbose_name_plural = "Réalisations"

    def __str__(self):
        return f"{self.titre} — {self.client or 'Client non défini'}"

    def save(self, *args, **kwargs):
        # Images servies en WebP redimensionné (les PNG d'origine pèsent ~600 Ko)
        compresser_image(self.image, max_width=1600)
        compresser_image(self.logo, max_width=256, quality=90)
        super().save(*args, **kwargs)