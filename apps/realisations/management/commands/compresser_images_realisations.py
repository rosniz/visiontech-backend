from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ancien nom conservé : utilisez désormais « compresser_images » (tout le site)."

    def handle(self, *args, **options):
        call_command('compresser_images', stdout=self.stdout)
