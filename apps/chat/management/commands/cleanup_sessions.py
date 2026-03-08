# ═══════════════════════════════════════════════════════════════════
# apps/chat/management/commands/cleanup_sessions.py
# Supprime les conversations inactives depuis plus de 30 minutes
# ═══════════════════════════════════════════════════════════════════
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.chat.models import Conversation


class Command(BaseCommand):
    help = 'Supprime les sessions chat inactives depuis plus de 30 minutes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--minutes', type=int, default=30,
            help='Durée en minutes avant expiration (défaut: 30)'
        )
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Simule sans supprimer'
        )

    def handle(self, *args, **options):
        minutes   = options['minutes']
        dry_run   = options['dry_run']
        threshold = timezone.now() - timedelta(minutes=minutes)

        # On garde les conversations humaines actives, on nettoie bot/pending expirées
        expired = Conversation.objects.filter(
            updated_at__lt=threshold,
            status__in=['bot', 'pending', 'closed']
        )

        count = expired.count()

        if dry_run:
            self.stdout.write(f'[DRY RUN] {count} session(s) seraient supprimées.')
            return

        expired.delete()
        self.stdout.write(
            self.style.SUCCESS(f'✅ {count} session(s) expirée(s) supprimées.')
        )