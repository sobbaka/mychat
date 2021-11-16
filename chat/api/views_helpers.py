from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from rest_framework.authtoken.models import Token

from chat.models import ChatRoom


def send_message_info(chat_id, user):
    channel_layer = get_channel_layer()
    chat = f'chat_{chat_id}'
    message = {
        'type': 'info_message',
        'username': user.username,
        'user_id': user.id,
        'flag': 'NEW'
    }
    async_to_sync(channel_layer.group_send)(chat, message)


def send_message(chat_id, user, text):
    channel_layer = get_channel_layer()
    chat = f'chat_{chat_id}'
    text = str(text)
    message = {
        'type': 'chat_message',
        'message': text,
        'username': f'{user.username}'
    }
    async_to_sync(channel_layer.group_send)(chat, message)


def signal_to_delete_user_from_chat_list(chat_id, user):
    channel_layer = get_channel_layer()
    chat = f'chat_{chat_id}'
    message = {
        'type': 'info_message',
        'username': user.username,
        'user_id': user.id,
        'flag': 'OFF'
    }
    async_to_sync(channel_layer.group_send)(chat, message)


def get_user_from_token(request):
    token = request.headers['Authorization'].strip('Token ')
    user = Token.objects.get(key=token).user
    return user


def get_chat_obj(request):
    try:
        chat_id = request.POST.get('chat_id')
        chat = ChatRoom.objects.get(id=chat_id)
        return chat
    except ChatRoom.DoesNotExist:
        return False