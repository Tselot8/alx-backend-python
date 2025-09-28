from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,   
    TokenRefreshView,
)
from chats.views import SignupView, test_admin_action

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),        # Chats app API
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/signup/", SignupView.as_view(), name="signup"),
    path("api/admin/some_action/", test_admin_action),
]