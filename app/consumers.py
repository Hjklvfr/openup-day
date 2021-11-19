import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        username = self.scope['session'].get('username', 'server')
        room_name = self.scope['url_route']['kwargs']['room_name']
        room_group_name = 'room_%s' % room_name

        # Join room group
        await self.channel_layer.group_add(
            room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.channel_layer.group_send(
            room_group_name,
            {
                'username': username,
                'online': True,
                'type': 'chat_message',  # todo change to connect
            }
        )

    async def disconnect(self, code):
        username = self.scope['session'].get('username', 'server')
        room_name = self.scope['url_route']['kwargs']['room_name']
        room_group_name = 'room_%s' % room_name

        await self.channel_layer.group_send(
            room_group_name,
            {
                'username': username,
                'online': False,
                'type': 'disconnect',
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        username = self.scope['session'].get('username', 'server')
        room_name = self.scope['url_route']['kwargs']['room_name']
        room_group_name = 'room_%s' % room_name

        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        chat_data = {
            'type': 'chat_message',
            'username': username,
        }

        if message:
            chat_data.update({'message': message})

        # Send message to room group
        await self.channel_layer.group_send(room_group_name, chat_data)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
