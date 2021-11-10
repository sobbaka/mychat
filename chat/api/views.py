from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from accounts.models import CustomUser
from chat.models import Message, ChatRoom
from .serializers import MessageSerializer, ChatRoomSerializer

from .views_helpers import get_user_from_token, get_chat_obj, send_message, send_message_info, \
	signal_to_delete_user_from_chat_list


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def api_get_chat_history(request, pk):
	user = get_user_from_token(request)
	users = ChatRoom.objects.get(pk=pk).users.all()
	if user not in users:
		return Response(status=status.HTTP_403_FORBIDDEN, data='Access for this user is not allowed')
	chat_history = Message.objects.filter(chatroom=pk)
	if chat_history:
		serializer = MessageSerializer(chat_history, many=True)
		return Response(serializer.data)
	return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_send_message(request):
	user = get_user_from_token(request)
	text = request.data['body']
	chat = get_chat_obj(request)
	if not chat:
		data = {}
		data['FAIL'] = 'CHAT DOES NOT EXIST'
		return Response(data=data, status=status.HTTP_404_NOT_FOUND)
	users = chat.users.all()
	if user not in users:
		return Response(status=status.HTTP_403_FORBIDDEN, data='Access for this user is not allowed')
	message = Message(not_websocket=True, user=user, chatroom=chat)
	if request.method == 'POST':
		serializer = MessageSerializer(message, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			chat_id = request.POST.get('chat_id')
			send_message(chat_id, user, text)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_chat(request):
	if request.method == 'POST':
		serializer = ChatRoomSerializer(data=request.data)
		#data = {}
		if serializer.is_valid():
			serializer.save()
			users_id = [int(id) for id in request.data['users'].split(',')]
			chat = ChatRoom.objects.get(pk=serializer.data['chat_id'])
			for id in users_id:
				user = CustomUser.objects.get(pk=id)
				chat.users.add(user)
				serializer.data['users'].append({'user': user.id, 'username': user.username})
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def api_enter_the_chat(request):
	user = get_user_from_token(request)
	chat = get_chat_obj(request)
	if not chat:
		data = {}
		data['FAIL'] = 'CHAT DOES NOT EXIST'
		return Response(data=data, status=status.HTTP_404_NOT_FOUND)
	if request.method == 'POST':
		chat.users.add(user)
		chat_id = request.POST.get('chat_id')
		send_message_info(chat_id, user)
		data = {}
		data['SUCCESS'] = 'UPDATE_SUCCESS'
		return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def api_leave_chat(request):
	user = get_user_from_token(request)
	chat = get_chat_obj(request)
	if not chat:
		data = {}
		data['FAIL'] = 'CHAT DOES NOT EXIST'
		return Response(data=data, status=status.HTTP_404_NOT_FOUND)
	if request.method == 'POST':
		chat.users.remove(user)
		chat_id = request.POST.get('chat_id')
		signal_to_delete_user_from_chat_list(chat_id, user)
		data = {}
		data['SUCCESS'] = 'UPDATE_SUCCESS'
		return Response(data=data, status=status.HTTP_200_OK)