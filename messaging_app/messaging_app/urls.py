# messaging_app/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),       # include your chats API endpoints
    path('api-auth/', include('rest_framework.urls')),  # DRF login for browsable API
]
