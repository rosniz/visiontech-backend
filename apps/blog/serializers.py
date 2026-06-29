from django.conf import settings
from rest_framework import serializers
from .models import Article, ArticleImage, Categorie, Tag
from .rendering import render_markdown

FRONTEND_URL = getattr(settings, 'FRONTEND_URL', 'https://visiontech.vision')


class CategorieSerializer(serializers.ModelSerializer):
    nb_articles = serializers.SerializerMethodField()

    class Meta:
        model  = Categorie
        fields = ['id', 'nom', 'slug', 'description', 'couleur', 'nb_articles']

    def get_nb_articles(self, obj):
        return obj.articles.publies().count()


class TagSerializer(serializers.ModelSerializer):
    nb_articles = serializers.SerializerMethodField()

    class Meta:
        model  = Tag
        fields = ['id', 'nom', 'slug', 'nb_articles']

    def get_nb_articles(self, obj):
        return obj.articles.publies().count()


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ArticleImage
        fields = ['id', 'image', 'legende', 'ordre']


# ── Liste (cartes) ──────────────────────────────────────────────────────────

class ArticleListSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)
    tags      = TagSerializer(many=True, read_only=True)

    class Meta:
        model  = Article
        fields = [
            'id', 'titre', 'slug', 'sous_titre', 'extrait', 'image_couverture',
            'categorie', 'tags', 'auteur_nom', 'auteur_avatar',
            'statut', 'date_publication', 'mis_en_avant',
            'temps_lecture', 'vues', 'created_at',
        ]


# ── Détail (page article) ────────────────────────────────────────────────────

class ArticleDetailSerializer(serializers.ModelSerializer):
    categorie         = CategorieSerializer(read_only=True)
    tags              = TagSerializer(many=True, read_only=True)
    galerie           = ArticleImageSerializer(many=True, read_only=True)
    contenu_html      = serializers.SerializerMethodField()
    table_des_matieres = serializers.SerializerMethodField()
    meta_titre_final       = serializers.SerializerMethodField()
    meta_description_final = serializers.SerializerMethodField()
    og_image_url            = serializers.SerializerMethodField()
    canonical_url_final     = serializers.SerializerMethodField()
    articles_similaires     = serializers.SerializerMethodField()

    class Meta:
        model  = Article
        fields = [
            'id', 'titre', 'slug', 'sous_titre', 'extrait',
            'contenu_html', 'table_des_matieres',
            'image_couverture', 'galerie',
            'categorie', 'tags', 'auteur_nom', 'auteur_avatar',
            'statut', 'date_publication', 'mis_en_avant',
            'temps_lecture', 'vues',
            'meta_titre_final', 'meta_description_final', 'og_image_url', 'canonical_url_final',
            'articles_similaires',
            'created_at', 'updated_at',
        ]

    def get_contenu_html(self, obj):
        html, _ = render_markdown(obj.contenu)
        return html

    def get_table_des_matieres(self, obj):
        _, toc = render_markdown(obj.contenu)
        return toc

    def get_meta_titre_final(self, obj):
        return obj.meta_titre or obj.titre

    def get_meta_description_final(self, obj):
        return obj.meta_description or obj.extrait

    def get_og_image_url(self, obj):
        request = self.context.get('request')
        img = obj.og_image or obj.image_couverture
        if not img:
            return None
        return request.build_absolute_uri(img.url) if request else img.url

    def get_canonical_url_final(self, obj):
        return obj.canonical_url or f'{FRONTEND_URL}/blog/{obj.slug}'

    def get_articles_similaires(self, obj):
        qs = Article.objects.publies().exclude(pk=obj.pk)
        if obj.categorie_id:
            qs = qs.filter(categorie_id=obj.categorie_id)
        qs = qs.order_by('-vues', '-date_publication')[:4]
        return ArticleListSerializer(qs, many=True, context=self.context).data


# ── Création / édition (admin) ───────────────────────────────────────────────

class ArticleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Article
        fields = [
            'titre', 'slug', 'sous_titre', 'extrait', 'contenu', 'image_couverture',
            'categorie', 'tags', 'auteur_nom', 'auteur_avatar',
            'statut', 'date_publication', 'mis_en_avant',
            'meta_titre', 'meta_description', 'og_image', 'canonical_url',
        ]
