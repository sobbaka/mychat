from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from mychat.views import chatRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('users/', include('accounts.urls')),
    path('api/chat/', include('chat.api.urls')),
    path('api/users/', include('accounts.api.urls')),
    path('accounts/', include('allauth.urls')),
    path('', chatRedirect)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)