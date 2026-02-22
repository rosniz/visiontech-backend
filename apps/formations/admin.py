from django.contrib import admin
from .models import Formation

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'niveau', 'duree', 'prix', 'created_at']
    list_filter = ['niveau', 'created_at']
    search_fields = ['titre', 'description_courte', 'description_complete']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'sous_titre', 'description_courte', 'description_complete')
        }),
        ('Détails', {
            'fields': ('duree', 'niveau', 'prix')
        }),
        ('Médias', {
            'fields': ('image', 'syllabus')
        }),
    )