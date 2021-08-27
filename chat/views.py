from django.shortcuts import render
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required

from chat.models import ChatRoom, Message


@login_required(login_url='/accounts/login/')
def index(request):
    chatrooms = ChatRoom.objects.all()
    return render(
        request,
        'chat/index.html',
        {
            'chatrooms': chatrooms,
        }
    )


@login_required(login_url='/accounts/login/')
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