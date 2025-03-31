import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message, ChatRoom
from authentications.models import User  # Import your custom user model
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Handle messages sent from WebSocket.
        - Save to DB
        - Send to room group
        """
        data = json.loads(text_data)
        message = data.get("message")
        user = self.scope["user"]

        if not user.is_authenticated:
            await self.send(text_data=json.dumps({"error": "Authentication required"}))
            return

        try:
            chat_room = await sync_to_async(ChatRoom.objects.get)(id=self.room_id)
        except ChatRoom.DoesNotExist:
            await self.send(text_data=json.dumps({"error": "Invalid room"}))
            return

        # Save message in DB
        message_obj = await sync_to_async(Message.objects.create)(
            user=user, room=chat_room, content=message
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_obj.content,
                "user": user.email if user.email else "Anonymous",
                "timestamp": str(message_obj.timestamp)
            },
        )

    async def chat_message(self, event):
        """Send message to WebSocket clients"""
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "user": event["user"],
            "timestamp": event["timestamp"]
        }))
