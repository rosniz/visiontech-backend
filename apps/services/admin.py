from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Interface d'administration simple pour les services"""
    
    list_display = ['titre', 'client', 'categorie', 'statut', 'ordre', 'lien', 'created_at']
    list_filter = ['categorie', 'statut', 'created_at']
    list_editable = ['ordre', 'statut', 'categorie']
    search_fields = ['nom', 'description_courte', 'description']
    ordering = ['ordre', '-created_at']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'description_courte', 'description', 'image')
        }),
        ('Détails', {
            'fields': ('points_forts', 'prix_a_partir_de', 'duree_estimee')
        }),
        ('Gestion', {
            'fields': ('est_actif', 'ordre')
        }),
    )