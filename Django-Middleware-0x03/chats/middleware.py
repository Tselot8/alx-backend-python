# Django-Middleware-0x03/chats/middleware.py
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.backends import TokenBackend
import logging

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Middleware initialization (called once)

    def __call__(self, request):
        # Get the user (anonymous if not logged in)
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log the request to file
        with open("requests.log", "a") as log_file:
            log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")

        # Call the next middleware / view
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the chat app between 6 PM and 9 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = 23  # 0-23

        # Deny access if current time is outside 6 AM - 9 PM
        if current_hour < 0 or current_hour < 23:
            return JsonResponse(
                {"error": "Chat access is allowed only between 6 AM and 9 PM."},
                status=403
            )

        response = self.get_response(request)
        return response
    
class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of chat messages sent per minute per IP.
    Works for both /api/messages/ and /add_message/ endpoints.
    """

    # Track requests in-memory (IP -> list of timestamps)
    request_history = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only track POST requests to message endpoints
        if request.method == "POST" and (
            "/api/messages/" in request.path or "/add_message/" in request.path
        ):
            ip = self.get_client_ip(request)
            now = datetime.now()
            history = self.request_history.get(ip, [])

            # Remove timestamps older than 1 minute
            history = [ts for ts in history if now - ts < timedelta(minutes=1)]

            if len(history) >= 5:
                # Limit exceeded
                return JsonResponse(
                    {"error": "You can only send 5 messages per minute."},
                    status=429
                )

            # Add current timestamp
            history.append(now)
            self.request_history[ip] = history

        # Continue processing the request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get IP address from headers or remote address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
    
User = get_user_model()
logger = logging.getLogger(__name__)

class RolePermissionMiddleware:
    """
    Middleware to enforce role-based access control.
    Only users with role 'admin' or 'moderator' can access certain endpoints.
    This middleware tries request.user first; if anonymous it will attempt
    to decode a Bearer JWT from the Authorization header.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def _decode_jwt_and_get_user(self, token_str):
        """Return User instance from token or None (raises on invalid token)."""
        try:
            token_backend = TokenBackend(
                algorithm=settings.SIMPLE_JWT.get("ALGORITHM", "HS256"),
                signing_key=settings.SIMPLE_JWT.get("SIGNING_KEY", settings.SECRET_KEY),
            )
            payload = token_backend.decode(token_str, verify=True)
            user_id_claim = settings.SIMPLE_JWT.get("USER_ID_CLAIM", "user_id")
            uid = payload.get(user_id_claim) or payload.get("user_id")
            if not uid:
                return None
            return User.objects.filter(user_id=uid).first()
        except Exception as exc:
            logger.debug("JWT decode failed in RolePermissionMiddleware: %s", exc)
            return None

    def __call__(self, request):
        # paths that require admin/moderator
        protected_paths = [
            "/api/admin/",
            "/api/users/",
        ]

        if any(request.path.startswith(path) for path in protected_paths):
            # If Django/Session auth already set a user, use it
            user = getattr(request, "user", None)
            if user and user.is_authenticated:
                role = getattr(user, "role", None)
                if role not in ["admin", "moderator"]:
                    return JsonResponse(
                        {"error": "You do not have permission to perform this action."},
                        status=403,
                    )
            else:
                # Try to read JWT from Authorization header
                auth = request.META.get("HTTP_AUTHORIZATION", "")
                if auth and auth.startswith("Bearer "):
                    token = auth.split(" ", 1)[1].strip()
                    user_obj = self._decode_jwt_and_get_user(token)
                    if not user_obj:
                        return JsonResponse({"error": "Authentication required."}, status=401)
                    # Check role
                    if getattr(user_obj, "role", None) not in ["admin", "moderator"]:
                        return JsonResponse(
                            {"error": "You do not have permission to perform this action."},
                            status=403,
                        )
                    # Attach user to request for downstream code
                    request.user = user_obj
                else:
                    return JsonResponse({"error": "Authentication required."}, status=401)

        response = self.get_response(request)
        return response