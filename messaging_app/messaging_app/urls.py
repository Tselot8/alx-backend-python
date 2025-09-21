# messaging_app/messaging_app/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views import ConversationViewSet, MessageViewSet  # <- correct import

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')  # <- typo fixed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
