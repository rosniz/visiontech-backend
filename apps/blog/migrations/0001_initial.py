import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, unique=True, verbose_name='Nom')),
                ('slug', models.SlugField(blank=True, max_length=120, unique=True)),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('couleur', models.CharField(default='#0ea5e9', max_length=7, verbose_name='Couleur (hex)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Catégorie',
                'verbose_name_plural': 'Catégories',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True, verbose_name='Nom')),
                ('slug', models.SlugField(blank=True, max_length=70, unique=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200, verbose_name='Titre')),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True)),
                ('sous_titre', models.CharField(blank=True, max_length=300, verbose_name='Sous-titre')),
                ('extrait', models.TextField(max_length=500, verbose_name='Extrait')),
                ('contenu', models.TextField(verbose_name='Contenu (Markdown)')),
                ('image_couverture', models.ImageField(blank=True, null=True, upload_to='blog/covers/', verbose_name='Image de couverture')),
                ('auteur_nom', models.CharField(default='VisionTech SARL', max_length=100, verbose_name='Auteur')),
                ('auteur_avatar', models.ImageField(blank=True, null=True, upload_to='blog/auteurs/', verbose_name='Avatar auteur')),
                ('statut', models.CharField(choices=[('brouillon', 'Brouillon'), ('programme', 'Programmé'), ('publie', 'Publié')], default='brouillon', max_length=20, verbose_name='Statut')),
                ('date_publication', models.DateTimeField(blank=True, null=True, verbose_name='Date de publication')),
                ('mis_en_avant', models.BooleanField(default=False, verbose_name="Mis en avant (page d'accueil du blog)")),
                ('temps_lecture', models.PositiveIntegerField(default=1, editable=False, verbose_name='Temps de lecture (min)')),
                ('vues', models.PositiveIntegerField(default=0, editable=False, verbose_name='Vues')),
                ('meta_titre', models.CharField(blank=True, max_length=70, verbose_name='Titre SEO')),
                ('meta_description', models.CharField(blank=True, max_length=160, verbose_name='Meta description')),
                ('og_image', models.ImageField(blank=True, null=True, upload_to='blog/og/', verbose_name='Image Open Graph')),
                ('canonical_url', models.URLField(blank=True, verbose_name='URL canonique')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categorie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='blog.categorie', verbose_name='Catégorie')),
                ('tags', models.ManyToManyField(blank=True, related_name='articles', to='blog.tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ['-date_publication', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='blog/gallery/')),
                ('legende', models.CharField(blank=True, max_length=200, verbose_name='Légende')),
                ('ordre', models.PositiveIntegerField(default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='galerie', to='blog.article')),
            ],
            options={
                'verbose_name': 'Image de galerie',
                'verbose_name_plural': 'Images de galerie',
                'ordering': ['ordre', 'id'],
            },
        ),
    ]
