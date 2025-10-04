# messaging/managers.py
from django.db import models
from .models import Message

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Returns unread messages for a specific user,
        optimized with only() to fetch necessary fields.
        """
        return self.filter(receiver=user, read=False)\
            .select_related('sender', 'receiver')\
            .prefetch_related('replies')\
            .only('id', 'sender', 'receiver', 'content', 'timestamp', 'read', 'parent_message')
