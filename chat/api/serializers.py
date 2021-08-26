from rest_framework import serializers
from chat.models import Message
from accounts.models import CustomUser

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

