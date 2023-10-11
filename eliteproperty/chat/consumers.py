# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.sender_id = int(self.scope['url_route']['kwargs']['send'])
            self.receiver_id = int(self.scope['url_route']['kwargs']['receive'])
            self.room_name = f"chat_{self.sender_id}_{self.receiver_id}"
            self.room_group_name = f"chat_{self.sender_id}_{self.receiver_id}"

            # Join the chat room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        except Exception as e:
            
            await self.close()


    async def disconnect(self, close_code):
        # Leave the chat room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message_data = json.loads(text_data)
        content = message_data['content']
        sender_id = message_data['sender']
        recipient_id = message_data['recipient']

        # Save the message to the database
        message = Message.objects.create(
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content
        )

        # Send message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'timestamp': message.timestamp.isoformat(),
                'sender_id': sender_id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        timestamp = event['timestamp']
        sender_id = event['sender_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'timestamp': timestamp,
            'sender_id': sender_id,
        }))