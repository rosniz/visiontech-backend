from django.core.management.base import BaseCommand

from core.images import compresser_image

# (app.Modèle, champ, largeur max) : mêmes réglages que la compression à l'enregistrement
CIBLES = [
    ('realisations.Realisation', 'image',            1600),
    ('realisations.Realisation', 'logo',             256),
    ('formations.Formation',     'image',            1400),
    ('services.Service',         'image',            1400),
    ('blog.Article',             'image_couverture', 1600),
    ('blog.Article',             'og_image',         1200),
    ('blog.ArticleImage',        'image',            1400),
]


class Command(BaseCommand):
    help = ("Convertit en WebP redimensionné toutes les images déjà envoyées "
            "(réalisations, formations, services, blog). À lancer une fois ; sans effet sur les images déjà en WebP.")

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help="Affiche ce qui serait converti, sans rien modifier.")

    def handle(self, *args, dry_run=False, **options):
        from django.apps import apps

        total = 0
        for label, champ, largeur in CIBLES:
            Modele = apps.get_model(label)
            for obj in Modele.objects.all():
                fichier = getattr(obj, champ)
                if not fichier or fichier.name.lower().endswith('.webp'):
                    continue
                avant = fichier.name
                if dry_run:
                    self.stdout.write(f'  [simulation] {label}#{obj.pk} {champ} : {avant}')
                    total += 1
                    continue
                compresser_image(fichier, max_width=largeur, quality=90 if champ == 'logo' else 82)
                if fichier.name != avant:
                    # update() plutôt que save() : pas de date de modification touchée, pas d'autre effet
                    Modele.objects.filter(pk=obj.pk).update(**{champ: fichier.name})
                    total += 1
                    self.stdout.write(f'  {label}#{obj.pk} {champ} : {avant} -> {fichier.name}')
                else:
                    self.stdout.write(self.style.WARNING(f'  {label}#{obj.pk} {champ} : impossible à convertir ({avant})'))

        verbe = 'à convertir' if dry_run else 'convertie(s)'
        self.stdout.write(self.style.SUCCESS(f'{total} image(s) {verbe}.'))
