from rest_framework import serializers

from accounts.api.serializers import UserInfoSerializer
from chat.models import Message, ChatRoom


class MessageSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=True)

    class Meta:
        model = Message
        fields = [
            'user',
            'user_username',
            'chatroom',
            'body',
            'timestamp'
        ]

    user_username = serializers.SerializerMethodField('get_user_username')

    def get_user_username(self, obj):
        return obj.user.username


class ChatRoomSerializer(serializers.ModelSerializer):
    users = UserInfoSerializer(many=True, read_only=False)

    class Meta:
        model = ChatRoom
        fields = [
            'name',
            'users'
        ]