import django_filters
from .models import Message, User

class MessageFilter(django_filters.FilterSet):
    # Filter messages by sender_id
    sender_id = django_filters.UUIDFilter(field_name='sender__user_id')
    # Filter messages by conversation_id
    conversation_id = django_filters.UUIDFilter(field_name='conversation__conversation_id')
    # Filter messages by date range
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender_id', 'conversation_id', 'start_date', 'end_date']
