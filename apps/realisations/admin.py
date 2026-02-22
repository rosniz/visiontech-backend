from django.contrib import admin
from .models import Realisation


@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    """Interface d'administration pour les réalisations"""

    list_display = ['titre', 'client', 'categorie', 'statut', 'ordre', 'lien', 'created_at']
    list_filter = ['categorie', 'statut', 'created_at']
    search_fields = ['titre', 'description', 'client', 'technologies']
    ordering = ['ordre', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['ordre', 'statut', 'categorie']

    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'description', 'image', 'lien')
        }),
        ('Client & Projet', {
            'fields': ('client', 'technologies', 'categorie', 'statut', 'ordre')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )