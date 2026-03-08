# apps/chat/scheduler.py
# Démarre un scheduler léger pour nettoyer les sessions toutes les 30 min
# Appelé depuis apps/chat/apps.py au démarrage de Django

from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

def cleanup_expired_sessions():
    """Supprime les conversations bot/pending inactives depuis 30 min."""
    try:
        from apps.chat.models import Conversation
        threshold = timezone.now() - timedelta(minutes=30)
        deleted, _ = Conversation.objects.filter(
            updated_at__lt=threshold,
            status__in=['bot', 'pending', 'closed']
        ).delete()
        if deleted:
            logger.info(f'Chat cleanup: {deleted} session(s) supprimée(s)')
    except Exception as e:
        logger.error(f'Chat cleanup error: {e}')


def start():
    scheduler = BackgroundScheduler(timezone='Africa/Douala')
    scheduler.add_job(
        cleanup_expired_sessions,
        trigger='interval',
        minutes=30,
        id='chat_session_cleanup',
        replace_existing=True,
    )
    scheduler.start()
    logger.info('✅ Chat session cleanup scheduler démarré (toutes les 30 min)')