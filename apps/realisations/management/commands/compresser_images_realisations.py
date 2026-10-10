from django.core.management.base import BaseCommand

from apps.realisations.models import Realisation


class Command(BaseCommand):
    help = "Convertit en WebP redimensionné les images de réalisations déjà envoyées (à lancer une fois)."

    def handle(self, *args, **options):
        total = 0
        for r in Realisation.objects.all():
            avant = (r.image.name if r.image else '', r.logo.name if r.logo else '')
            r.save()
            apres = (r.image.name if r.image else '', r.logo.name if r.logo else '')
            if avant != apres:
                total += 1
                self.stdout.write(f'  {r.titre[:50]} : {avant[0]} -> {apres[0]}')
        self.stdout.write(self.style.SUCCESS(f'{total} réalisation(s) optimisée(s).'))
