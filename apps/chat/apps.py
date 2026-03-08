# apps/chat/apps.py
from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.chat'
    verbose_name = 'Chat Support'

    def ready(self):
        # Démarre le scheduler de nettoyage des sessions au démarrage Django
        try:
            from apps.chat.scheduler import start
            start()
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f'Scheduler not started: {e}')