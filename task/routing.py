# routing.py

from django.urls import path
from your_app.consumers import PushNotificationConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/notifications/', PushNotificationConsumer.as_asgi()),
    ]),
})
