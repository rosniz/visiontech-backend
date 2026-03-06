import os
import django

# 1. Configurer les settings EN PREMIER
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 2. Initialiser Django AVANT tout import de modèles/apps
django.setup()

# 3. Seulement après, importer Channels et le routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.chat.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            apps.chat.routing.websocket_urlpatterns
        )
    ),
})