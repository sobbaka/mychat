from django.forms import TextInput, EmailInput, FileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'image')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'image',)

        widgets = {
            'username': TextInput(attrs={'class': "form-control mb-2"}),
            'email': EmailInput(attrs={'class': "form-control mb-2"}),
            'image': FileInput(attrs={'class': "form-control-file"})
        }
