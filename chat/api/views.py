from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from accounts.models import CustomUser
from chat.models import Message, ChatRoom
from .serializers import MessageSerializer, ChatRoomSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

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