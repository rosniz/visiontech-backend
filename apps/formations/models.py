from django.db import models
from cloudinary.models import CloudinaryField

class Formation(models.Model):
    """Modèle pour les formations proposées par VisionTech"""
    
    # Informations principales
    titre = models.CharField(max_length=200, verbose_name="Titre")
    sous_titre = models.CharField(max_length=300, verbose_name="Sous-titre", blank=True)
    description_courte = models.TextField(max_length=500, verbose_name="Description courte", help_text="Résumé pour la liste")
    description_complete = models.TextField(verbose_name="Description complète")
    
     # Médias
    image = CloudinaryField('image', folder='formations/', blank=True, null=True)
    syllabus = CloudinaryField(
        'file', 
        folder='formations/syllabus/', 
        blank=True, 
        null=True, 
        resource_type='raw',
        type='upload'  # Force le type upload (public par défaut)
    )
    
    # Détails formation
    duree = models.CharField(max_length=100, verbose_name="Durée", blank=True, help_text="Ex: 3 mois, 40 heures")
    niveau = models.CharField(max_length=50, verbose_name="Niveau", blank=True, help_text="Ex: Débutant, Intermédiaire")
    
    # Prix optionnel
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix (FCFA)",
        blank=True,
        null=True
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
    
    def __str__(self):
        return self.titre