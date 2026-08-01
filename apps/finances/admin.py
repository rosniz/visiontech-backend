from django.contrib import admin
from .models import Budget, Charge, FinanceProfile, TypeCharge


@admin.register(FinanceProfile)
class FinanceProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'actif', 'created_at']
    list_filter = ['role', 'actif']
    list_editable = ['role', 'actif']
    search_fields = ['user__email', 'user__username']
    autocomplete_fields = ['user']


@admin.register(TypeCharge)
class TypeChargeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'actif']
    list_filter = ['categorie', 'actif']
    list_editable = ['actif']
    search_fields = ['nom', 'description']
    ordering = ['categorie', 'nom']


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'categorie', 'type_charge', 'montant', 'date_charge', 'statut', 'created_by']
    list_filter = ['categorie', 'statut', 'mode_paiement', 'date_charge']
    search_fields = ['libelle', 'beneficiaire', 'reference_piece']
    ordering = ['-date_charge']
    date_hierarchy = 'date_charge'
    autocomplete_fields = ['type_charge']

    fieldsets = (
        ('Classification', {
            'fields': ('categorie', 'type_charge')
        }),
        ('Détails', {
            'fields': ('libelle', 'montant', 'date_charge', 'beneficiaire', 'reference_piece', 'mode_paiement', 'statut')
        }),
        ('Compléments', {
            'fields': ('justificatif', 'details', 'notes')
        }),
        ('Suivi', {
            'fields': ('created_by',)
        }),
    )


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['categorie', 'annee', 'mois', 'montant_prevu', 'seuil_alerte', 'created_by']
    list_filter = ['categorie', 'annee']
    ordering = ['-annee', '-mois', 'categorie']
