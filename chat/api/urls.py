from django.urls import path
from .views import (
    api_get_chat_history,
    api_sent_message,
    api_create_chat
)

app_name = 'chat'

urlpatterns = [
    path('create_chat/', api_create_chat, name="api_create_chat"),
    path('create/', api_sent_message, name="sent_message"),
    path('<pk>/', api_get_chat_history, name="detail"),

]
