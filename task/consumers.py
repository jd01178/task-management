# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PushNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the user to the WebSocket group (optional, you can implement user-specific notifications)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the WebSocket group (optional)
        pass

    async def notify(self, event):
        # Send the notification to the client
        notification = event['notification']
        await self.send(text_data=json.dumps(notification))
