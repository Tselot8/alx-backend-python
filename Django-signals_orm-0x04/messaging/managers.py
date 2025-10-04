from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        # Only fetch unread messages and optimize fields
        return self.filter(receiver=user, read=False).only(
            'id', 'sender', 'receiver', 'content', 'timestamp', 'read', 'parent_message'
        )
