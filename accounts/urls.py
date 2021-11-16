from django.urls import path
from .views import CustomUserDetail, CustomUserUpdate


urlpatterns = [
    path('<int:pk>/edit/', CustomUserUpdate.as_view(), name='user_update'),
    path('<int:pk>/', CustomUserDetail.as_view(), name='user_detail'),
]