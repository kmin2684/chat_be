"""
ASGI config for chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application
application = get_asgi_application()

from WebSocket.middleware import TokenAuthMiddleware
import os
import django 
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import WebSocket.routing
from WebSocket.middleware import TokenAuthMiddleware



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")

django.setup()



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