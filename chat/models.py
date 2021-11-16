from django.db import models
from django.urls import reverse

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

import json

from accounts.models import CustomUser


class ChatRoom(models.Model):
    name = models.CharField(max_length=55, verbose_name='Имя чата', unique=True)
    users = models.ManyToManyField(
        CustomUser,
        verbose_name='Пользователи',
        related_name='user_chatrooms',
        null=True
    )

    def __str__(self):
        return f'{self.name} - {self.id}'

    def get_absolute_url(self):
        return reverse('room_detail', kwargs={"pk": self.id})


class Message(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name="Пользователь",
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_messages'
    )
    chatroom = models.ForeignKey(
        ChatRoom,
        verbose_name="Чат",
        on_delete=models.CASCADE,
        related_name='chatroom_messages'
    )
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, )
    not_websocket = models.BooleanField(default=True)

    def sent_message(self):
        channel_layer = get_channel_layer()
        chat = self.chatroom.name # Change this to chat ID ??
        message = {
            'type': 'chat_message',
            'message': f'{self.body}',
            'username': f'{self.user.username}'
        }
        async_to_sync(channel_layer.group_send)(chat, message)

    def save(self, *args, **kwargs):
        self.body = self.body.strip()
        if self.id is None and self.not_websocket:
            self.sent_message()
        super(Message, self).save(*args, **kwargs)