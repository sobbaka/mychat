from django import forms
from .models import ChatRoom
from allauth.account.forms import LoginForm


class NewLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(NewLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'class': 'form-control allauth-input', 'placeholder': 'Login'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control allauth-input', 'placeholder': 'Password'})

        self.fields["login"].label = ""
        self.fields["password"].label = ""


class ChatRoomForm(forms.ModelForm):

    class Meta:
        model = ChatRoom
        fields = ('name',)