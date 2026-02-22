from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField


class Service(models.Model):
    """Modèle simplifié pour les services VisionTech"""
    
    # Informations de base
    nom = models.CharField(max_length=200, verbose_name="Nom du service")
    description_courte = models.CharField(
        max_length=255, 
        verbose_name="Description courte",
        help_text="Résumé en une phrase"
    )
    description = models.TextField(verbose_name="Description détaillée")
    
    # Visuel
    image = CloudinaryField('image', folder='services/', blank=True, null=True)
    
    # Caractéristiques
    points_forts = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Points forts",
        help_text="Liste des avantages (ex: ['Point 1', 'Point 2'])"
    )
    
    # Tarification
    prix_a_partir_de = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Prix à partir de (FCFA)",
        validators=[MinValueValidator(0)]
    )
    duree_estimee = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Durée estimée",
        help_text="Ex: '2-4 semaines'"
    )
    
    # Gestion
    est_actif = models.BooleanField(
        default=True,
        verbose_name="Service actif"
    )
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['ordre', '-created_at']
        verbose_name = "Service"
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.nom