import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]

        print(f'self.room_name is ***{self.room_name }***')

        @database_sync_to_async
        def chat_get_or_create(room_name):
            return ChatRoom.objects.get_or_create(
                id=room_name
            )[0]

        self.chat_object = await chat_get_or_create(self.room_name)

        @database_sync_to_async
        def add_user_to_chat(chat, user):
            if not chat.users.filter(pk=user.id):
                chat.users.add(user)

        await add_user_to_chat(self.chat_object, self.user)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user.username} is here!',
                'username': f'{self.user.username}'
            })

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'info_message',
                'username': self.user.username,
                'user_id': self.user.id,
                'flag': 'NEW'
            })

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        @database_sync_to_async
        def delete_user_from_chat(chat, user):
            chat.users.remove(user)

        await delete_user_from_chat(self.chat_object, self.user)


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'info_message',
                'username': self.user.username,
                'user_id': self.user.id,
                'flag': 'OFF'
            })

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']


        # save message
        @database_sync_to_async
        def save_message_from_websocket(user, chatroom, body):
            chatroom = ChatRoom.objects.get(pk=chatroom)
            return Message.objects.create(user=user, chatroom=chatroom, body=body, not_websocket = False)

        self.message_object = await save_message_from_websocket(self.user, self.room_name, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': f'{self.user.username}'
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def info_message(self, event):
        username = event['username']
        user_id = event['user_id']
        flag = event['flag']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'username': username,
            'user_id': user_id,
            'flag': flag
        }))
