from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required

from chat.models import ChatRoom, Message
from chat.forms import ChatRoomForm

def error_404(request, exception=None):
    return render(request, 'chat/error_404.html', status=404)

@login_required(login_url='/accounts/login/')
def index(request):

    if request.method == 'GET':
        chatrooms = ChatRoom.objects.all()
        form = ChatRoomForm()
        return render(
            request,
            'chat/index.html',
            {
                'chatrooms': chatrooms,
                'form': form
            }
        )

    if request.method == 'POST':
        name = request.POST['name']
        name = f'room {len(ChatRoom.objects.all())}' if not name else name
        chatroom = ChatRoom.objects.get_or_create(name=name)[0]
        chatroom.users.add(request.user)
        return HttpResponseRedirect(f'/chat/{chatroom.id}/')


@login_required(login_url='/accounts/login/')
def room(request, pk):
    chat = get_object_or_404(ChatRoom, pk=pk)

    try:
        users = ChatRoom.objects.get(id=pk).users.all()
    except ObjectDoesNotExist:
        users = []

    messages = serialize(
        'json',
        Message.objects.filter(chatroom__id=pk),
        use_natural_foreign_keys=True,
    )

    return render(request, 'chat/room.html', {
        'room_name': pk,
        'users': users,
        'messages': messages,
        'chat': chat
    })