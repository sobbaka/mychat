from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.models import Token

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from chat.models import Message, ChatRoom
from .serializers import MessageSerializer, ChatRoomSerializer
# from accounts.models import CustomUser


@api_view(['GET', ])
def api_get_chat_history(request, pk):

	try:
		chat_history = Message.objects.filter(chatroom=pk)
	except Message.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = MessageSerializer(chat_history, many=True)
		return Response(serializer.data)


@api_view(['POST'])
def api_sent_message(request):

	message = Message(not_websocket=True)

	if request.method == 'POST':
		serializer = MessageSerializer(message, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_create_chat(request):

	if request.method == 'POST':

		serializer = ChatRoomSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def sent_message(chat_id, user):
	channel_layer = get_channel_layer()
	chat = f'chat_{chat_id}'
	message = {
		'type': 'info_message',
		'username': user.username,
		'user_id': user.id,
		'flag': 'NEW'
	}
	async_to_sync(channel_layer.group_send)(chat, message)


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def api_enter_the_chat(request):
	token = request.headers['Authorization'].strip('Token ')

	try:
		chat_id = request.POST.get('chat_id')
		chat = ChatRoom.objects.get(id=chat_id)
	except ChatRoom.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	try:
		user = Token.objects.get(key=token).user
	except ChatRoom.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'POST':
		try:
			chat.users.add(user)
			sent_message(chat_id, user)
			data = {}
			data['SUCCESS'] = 'UPDATE_SUCCESS'
		except ChatRoom.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		return Response(data=data)