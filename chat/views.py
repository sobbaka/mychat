from django.shortcuts import render
from django.core.serializers import serialize
from chat.models import ChatRoom, Message


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    users = ChatRoom.objects.get(name=f'chat_{room_name}').users.all()

    messages = serialize(
        'json',
        Message.objects.filter(chatroom__name=f'chat_{room_name}'),
        use_natural_foreign_keys=True,
    )

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'users': users,
        'messages': messages
    })