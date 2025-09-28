from rest_framework.permissions import BasePermission
from .models import Conversation, Message
from rest_framework import permissions

class IsParticipantOfConversation(BasePermission):
    """
    Allow only authenticated users.
    Only conversation participants can access or modify messages.
    """

    def has_permission(self, request, view):
        # Must be authenticated
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Conversation-level permissions
        if isinstance(obj, Conversation):
            # Only participants can retrieve, update, destroy, or add messages
            if view.action in ['retrieve', 'update', 'destroy', 'add_message']:
                return request.user in obj.participants.all()
            # List and creation allowed if authenticated
            return True

        # Message-level permissions
        if isinstance(obj, Message):
            # Only sender or conversation participants
            return request.user == obj.sender or request.user in obj.conversation.participants.all()

        return False
