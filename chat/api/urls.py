from django.urls import path
from .views import (
    api_get_chat_history,
    api_send_message,
    api_create_chat,
    api_enter_the_chat,
    api_leave_chat
)

app_name = 'chat'

urlpatterns = [
    path('enter_chat/', api_enter_the_chat, name="api_enter_the_chat"),
    path('create_chat/', api_create_chat, name="api_create_chat"),
    path('send_message/', api_send_message, name="api_send_message"),
    path('leave_chat/', api_leave_chat, name="api_leave_chat"),
    path('<pk>/', api_get_chat_history, name="api_get_chat_history"),
]

