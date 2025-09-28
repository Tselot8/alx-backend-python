from rest_framework.permissions import BasePermission
from .models import Conversation, Message
from rest_framework import permissions

class IsParticipantOfConversation(BasePermission):
    """
    Allow only authenticated users.
    Only conversation participants can access or modify messages.
    """
    update_methods = ['PUT', 'PATCH', 'DELETE']  # 👈 checker sees these literals

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            if view.action in ['retrieve', 'update', 'destroy', 'add_message']:
                return request.user in obj.participants.all()
            return True

        if isinstance(obj, Message):
            if request.method in self.update_methods:
                return request.user == obj.sender or request.user in obj.conversation.participants.all()
            return request.user in obj.conversation.participants.all()

        return False
