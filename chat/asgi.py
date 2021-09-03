"""
ASGI config for chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

from WebSocket.middleware import TokenAuthMiddleware
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import WebSocket.routing
from WebSocket.middleware import TokenAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")

# application = get_asgi_application()

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": TokenAuthMiddleware(
        URLRouter(
            WebSocket.routing.websocket_urlpatterns
        )
    ),
})

# application = ProtocolTypeRouter({
#   "http": get_asgi_application(),
#   "websocket": URLRouter(WebSocket.routing.websocket_urlpatterns),
# })