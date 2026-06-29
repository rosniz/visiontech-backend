import re
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.db.models import F


def _compresser_image(image_field, max_width=1600, quality=82):
    """Redimensionne et compresse une image uploadée (in-place sur le champ)."""
    if not image_field or image_field.name.lower().endswith('.webp'):
        return
    try:
        img = Image.open(image_field)
        img_format = 'WEBP' if img.format != 'GIF' else 'GIF'
        if img.mode in ('RGBA', 'P') and img_format == 'WEBP':
            img = img.convert('RGB')
        if img.width > max_width:
            ratio = max_width / float(img.width)
            img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format=img_format, quality=quality, optimize=True)
        name = image_field.name.rsplit('.', 1)[0] + '.webp'
        image_field.save(name, ContentFile(buffer.getvalue()), save=False)
    except Exception:
        pass


def _unique_slug(model_cls, base_slug, instance_pk=None):
    slug = base_slug
    i = 1
    qs = model_cls.objects.exclude(pk=instance_pk) if instance_pk else model_cls.objects.all()
    while qs.filter(slug=slug).exists():
        i += 1
        slug = f'{base_slug}-{i}'
    return slug


class Categorie(models.Model):
    nom         = models.CharField(max_length=100, unique=True, verbose_name='Nom')
    slug        = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Description')
    couleur     = models.CharField(max_length=7, default='#0ea5e9', verbose_name='Couleur (hex)')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(Categorie, slugify(self.nom), self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Tag(models.Model):
    nom  = models.CharField(max_length=50, unique=True, verbose_name='Nom')
    slug = models.SlugField(max_length=70, unique=True, blank=True)

    class Meta:
        ordering = ['nom']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(Tag, slugify(self.nom), self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class ArticleQuerySet(models.QuerySet):
    def publies(self):
        return self.filter(statut='publie', date_publication__lte=timezone.now())


class Article(models.Model):

    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('programme', 'Programmé'),
        ('publie',    'Publié'),
    ]

    # Contenu
    titre        = models.CharField(max_length=200, verbose_name='Titre')
    slug         = models.SlugField(max_length=220, unique=True, blank=True)
    sous_titre   = models.CharField(max_length=300, blank=True, verbose_name='Sous-titre')
    extrait      = models.TextField(max_length=500, verbose_name='Extrait', help_text='Description courte affichée dans les cartes et les meta tags')
    contenu      = models.TextField(verbose_name='Contenu (Markdown)')
    image_couverture = models.ImageField(upload_to='blog/covers/', blank=True, null=True, verbose_name='Image de couverture')

    # Classification
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', verbose_name='Catégorie')
    tags      = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name='Tags')

    # Auteur
    auteur_nom    = models.CharField(max_length=100, default='VisionTech SARL', verbose_name='Auteur')
    auteur_avatar = models.ImageField(upload_to='blog/auteurs/', blank=True, null=True, verbose_name='Avatar auteur')

    # Publication
    statut            = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon', verbose_name='Statut')
    date_publication   = models.DateTimeField(null=True, blank=True, verbose_name='Date de publication', help_text='Laisser vide = publication immédiate à la sauvegarde si statut = Publié')
    mis_en_avant       = models.BooleanField(default=False, verbose_name='Mis en avant (page d\'accueil du blog)')

    # Stats (auto)
    temps_lecture = models.PositiveIntegerField(default=1, editable=False, verbose_name='Temps de lecture (min)')
    vues          = models.PositiveIntegerField(default=0, editable=False, verbose_name='Vues')

    # SEO
    meta_titre       = models.CharField(max_length=70, blank=True, verbose_name='Titre SEO', help_text='Si vide : utilise le titre de l\'article')
    meta_description = models.CharField(max_length=160, blank=True, verbose_name='Meta description', help_text='Si vide : utilise l\'extrait')
    og_image         = models.ImageField(upload_to='blog/og/', blank=True, null=True, verbose_name='Image Open Graph', help_text='Si vide : utilise l\'image de couverture')
    canonical_url    = models.URLField(blank=True, verbose_name='URL canonique', help_text='Si vide : générée automatiquement')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ArticleQuerySet.as_manager()

    class Meta:
        ordering = ['-date_publication', '-created_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(Article, slugify(self.titre), self.pk)

        # Mots -> temps de lecture (≈200 mots/min, min 1 min)
        mots = len(re.findall(r'\w+', self.contenu or ''))
        self.temps_lecture = max(1, round(mots / 200))

        # Publication immédiate si statut publié sans date
        if self.statut == 'publie' and not self.date_publication:
            self.date_publication = timezone.now()

        _compresser_image(self.image_couverture, max_width=1600)
        _compresser_image(self.og_image, max_width=1200)

        super().save(*args, **kwargs)

    def incrementer_vues(self):
        Article.objects.filter(pk=self.pk).update(vues=F('vues') + 1)
        self.refresh_from_db(fields=['vues'])

    @property
    def est_publie(self):
        return self.statut == 'publie' and self.date_publication and self.date_publication <= timezone.now()


class ArticleImage(models.Model):
    """Galerie d'images intégrables dans le contenu d'un article."""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='galerie')
    image   = models.ImageField(upload_to='blog/gallery/')
    legende = models.CharField(max_length=200, blank=True, verbose_name='Légende')
    ordre   = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre', 'id']
        verbose_name = 'Image de galerie'
        verbose_name_plural = 'Images de galerie'

    def save(self, *args, **kwargs):
        _compresser_image(self.image, max_width=1400)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.article.titre} — image {self.ordre}'
