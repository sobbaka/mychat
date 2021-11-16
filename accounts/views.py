from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from .models import CustomUser
from .forms import CustomUserChangeForm

# Create your views here.
class CustomUserDetail(DetailView):

    model = CustomUser
    context_object_name = 'user'
    template_name = 'accounts/custom_user_detail.html'


class CustomUserUpdate(UpdateView):
    template_name = 'accounts/custom_user_update.html'
    form_class = CustomUserChangeForm

    context_object_name = 'user'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return CustomUser.objects.get(pk=id)