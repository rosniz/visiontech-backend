from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Interface d'administration simple pour les services"""
    
    list_display = ['nom', 'prix_a_partir_de', 'duree_estimee', 'est_actif', 'ordre', 'created_at']
    list_filter = ['est_actif', 'created_at']
    list_editable = ['ordre', 'est_actif']
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