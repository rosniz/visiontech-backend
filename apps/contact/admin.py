from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Interface d'administration pour les messages de contact"""
    
    list_display = ['nom', 'email', 'lu', 'date']
    list_filter = ['lu', 'date']
    search_fields = ['nom', 'email', 'message']
    ordering = ['-date']
    readonly_fields = ['date']
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Action pour marquer les messages comme lus"""
        updated = queryset.update(lu=True)
        self.message_user(request, f"{updated} message(s) marqué(s) comme lu(s)")
    mark_as_read.short_description = "Marquer comme lu"
    
    def mark_as_unread(self, request, queryset):
        """Action pour marquer les messages comme non lus"""
        updated = queryset.update(lu=False)
        self.message_user(request, f"{updated} message(s) marqué(s) comme non lu(s)")
    mark_as_unread.short_description = "Marquer comme non lu"
    
    fieldsets = (
        ('Informations du contact', {
            'fields': ('nom', 'email')
        }),
        ('Message', {
            'fields': ('message', 'lu')
        }),
        ('Date', {
            'fields': ('date',),
            'classes': ('collapse',)
        }),
    )
