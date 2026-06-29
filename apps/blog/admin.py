from django.contrib import admin
from django.utils.html import format_html
from .models import Article, ArticleImage, Categorie, Tag

STATUT_COLORS = {
    'brouillon': '#94a3b8',
    'programme': '#f59e0b',
    'publie':    '#22c55e',
}


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'slug', 'badge_couleur', 'nb_articles']
    search_fields = ['nom']
    prepopulated_fields = {'slug': ('nom',)}

    def badge_couleur(self, obj):
        return format_html(
            '<span style="display:inline-block;width:18px;height:18px;border-radius:4px;background:{0};border:1px solid #0003"></span> {0}',
            obj.couleur
        )
    badge_couleur.short_description = 'Couleur'

    def nb_articles(self, obj):
        return obj.articles.count()
    nb_articles.short_description = "Nb d'articles"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'slug', 'nb_articles']
    search_fields = ['nom']
    prepopulated_fields = {'slug': ('nom',)}

    def nb_articles(self, obj):
        return obj.articles.count()
    nb_articles.short_description = "Nb d'articles"


class ArticleImageInline(admin.TabularInline):
    model  = ArticleImage
    extra  = 1
    fields = ['image', 'legende', 'ordre']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display  = [
        'titre', 'categorie', 'statut_badge', 'auteur_nom',
        'date_publication', 'temps_lecture', 'vues_display', 'mis_en_avant',
    ]
    list_filter   = ['statut', 'categorie', 'tags', 'mis_en_avant']
    search_fields = ['titre', 'extrait', 'contenu']
    filter_horizontal = ['tags']
    prepopulated_fields = {'slug': ('titre',)}
    readonly_fields = ['temps_lecture', 'vues', 'created_at', 'updated_at']
    inlines = [ArticleImageInline]
    date_hierarchy = 'date_publication'
    save_on_top = True

    fieldsets = (
        ('📝 Contenu', {
            'fields': ('titre', 'slug', 'sous_titre', 'extrait', 'contenu', 'image_couverture')
        }),
        ('🏷️ Classification', {
            'fields': ('categorie', 'tags', 'mis_en_avant')
        }),
        ('👤 Auteur', {
            'fields': ('auteur_nom', 'auteur_avatar')
        }),
        ('🚀 Publication', {
            'fields': ('statut', 'date_publication'),
            'description': 'Programmé = publication automatique à la date choisie. Publié sans date = publication immédiate.',
        }),
        ('🔍 SEO', {
            'fields': ('meta_titre', 'meta_description', 'og_image', 'canonical_url'),
            'classes': ('collapse',),
        }),
        ('📊 Statistiques', {
            'fields': ('temps_lecture', 'vues', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def statut_badge(self, obj):
        color = STATUT_COLORS.get(obj.statut, '#64748b')
        return format_html(
            '<span style="padding:3px 10px;border-radius:20px;background:{0}20;'
            'color:{0};font-weight:700;font-size:12px;border:1px solid {0}40">{1}</span>',
            color, obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'

    def vues_display(self, obj):
        return format_html('👁️ {}', obj.vues)
    vues_display.short_description = 'Vues'

    actions = ['publier_maintenant', 'depublier']

    def publier_maintenant(self, request, queryset):
        from django.utils import timezone
        n = 0
        for article in queryset:
            article.statut = 'publie'
            article.date_publication = timezone.now()
            article.save()
            n += 1
        self.message_user(request, f'{n} article(s) publié(s).')
    publier_maintenant.short_description = '🚀 Publier maintenant'

    def depublier(self, request, queryset):
        n = queryset.update(statut='brouillon')
        self.message_user(request, f'{n} article(s) repassé(s) en brouillon.')
    depublier.short_description = '📥 Repasser en brouillon'
