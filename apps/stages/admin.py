from django.contrib import admin
from django.utils.html import format_html
from .models import DemandeStage
from .emails import send_status_update_email

STATUT_COLORS = {
    'en_attente': '#f59e0b',
    'en_etude':   '#3b82f6',
    'accepte':    '#22c55e',
    'refuse':     '#ef4444',
}


@admin.register(DemandeStage)
class DemandeStageAdmin(admin.ModelAdmin):

    list_display  = [
        'prenom', 'nom', 'email_contact', 'type_stage_badge',
        'domaine_badge', 'date_debut', 'date_fin',
        'statut_badge', 'created_at',
    ]
    list_filter   = ['statut', 'type_stage', 'domaine', 'created_at']
    search_fields = ['nom', 'prenom', 'email_contact']
    readonly_fields = ['created_at', 'updated_at']
    ordering      = ['-created_at']

    fieldsets = (
        ('👤 Informations personnelles', {
            'fields': ('user', 'prenom', 'nom', 'telephone', 'email_contact')
        }),
        ('🎓 Stage souhaité', {
            'fields': ('type_stage', 'domaine', 'date_debut', 'date_fin')
        }),
        ('📄 Documents', {
            'fields': ('cni_recto', 'cni_verso', 'carte_etudiant', 'certificat_scolarite', 'cv')
        }),
        ('✉️ Motivation', {
            'fields': ('lettre_motivation',)
        }),
        ('⚙️ Gestion administrative', {
            'fields': ('statut', 'commentaire_admin'),
            'description': 'Modifiez le statut et ajoutez un message. Un email sera envoyé automatiquement.',
        }),
        ('🕒 Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['envoyer_notification_email']

    def statut_badge(self, obj):
        color = STATUT_COLORS.get(obj.statut, '#64748b')
        return format_html(
            '<span style="padding:3px 10px;border-radius:20px;background:{0}20;'
            'color:{0};font-weight:700;font-size:12px;border:1px solid {0}40">{1}</span>',
            color, obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'

    def type_stage_badge(self, obj):
        colors = {
            'vacances':         '#0ea5e9',
            'pre_emploi':       '#8b5cf6',
            'perfectionnement': '#10b981',
        }
        color = colors.get(obj.type_stage, '#64748b')
        return format_html(
            '<span style="padding:2px 8px;border-radius:6px;background:{0}20;'
            'color:{0};font-size:12px;font-weight:600">{1}</span>',
            color, obj.get_type_stage_display()
        )
    type_stage_badge.short_description = 'Type'

    def domaine_badge(self, obj):
        if not obj.domaine:
            return '—'
        return format_html(
            '<span style="padding:2px 8px;border-radius:6px;background:#e0f2fe;'
            'color:#0369a1;font-size:12px">{}</span>',
            obj.get_domaine_display()
        )
    domaine_badge.short_description = 'Domaine'

    def save_model(self, request, obj, form, change):
        if change and 'statut' in form.changed_data:
            super().save_model(request, obj, form, change)
            try:
                send_status_update_email(obj)
                self.message_user(request, f'Email de notification envoyé à {obj.email_contact}.')
            except Exception as e:
                self.message_user(request, f'Statut mis à jour mais email non envoyé : {e}', level='warning')
        else:
            super().save_model(request, obj, form, change)

    def envoyer_notification_email(self, request, queryset):
        ok, ko = 0, 0
        for demande in queryset:
            try:
                send_status_update_email(demande)
                ok += 1
            except Exception:
                ko += 1
        if ok:
            self.message_user(request, f'Email envoyé à {ok} candidat(s).')
        if ko:
            self.message_user(request, f'{ko} email(s) non envoyé(s).', level='warning')
    envoyer_notification_email.short_description = '📧 Envoyer notification email'
