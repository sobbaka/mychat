from django.urls import path
from chat.views import index, room



urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>/', room, name='room_detail')
]