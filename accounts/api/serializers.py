from rest_framework import serializers
from accounts.models import CustomUser


# TODO password2 doesn`t work. Save mathod doesn`t work
class RegistrationSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
        # fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def save(self):
            account = CustomUser(
                email=self.validated_data['email'],
                username=self.validated_data['username']
            )
            password = self.validated_data['password']
            password2 = self.validated_data['password2']
            if password != password2:
                raise serializers.ValidationError({'password': 'Passwords must match.'})
            account.set_password(password)
            account.save()
            return account
