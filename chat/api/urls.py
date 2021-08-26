from django.urls import path
from .views import (
    api_get_chat_history,
    api_sent_message
)

app_name = 'chat'

urlpatterns = [
    path('create/', api_sent_message, name="sent_message"),
    path('<pk>/', api_get_chat_history, name="detail"),

]

