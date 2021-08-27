from django.urls import path

from chat.views import index, room

urlpatterns = [
    path('', index),
    path('<int:room_name>/', room, name='room_detail')
]
