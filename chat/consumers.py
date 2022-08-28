import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.http import JsonResponse

from .models import Message, Room

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        print(self.user)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("receive() called")
        text_data_json = json.loads(text_data)
        message_body = text_data_json['message']

        # save message to database
       
        message = await self.save_message(message_body)
    
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.body,
                'sender': message.sender.username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print("chat_message() called", event)
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    
    # database methods
    @database_sync_to_async
    def save_message(self, message_body):
        room = Room.objects.get(name=self.room_name)
        message = Message.objects.create(sender=self.user, body=message_body, room=room)
        print("message saved")
        return message