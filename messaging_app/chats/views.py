from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


# -----------------------
# Conversation ViewSet
# -----------------------
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Provides endpoints to list conversations and create a new conversation.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['participants']
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        """
        Custom action to send a message to an existing conversation.
        """
        conversation = self.get_object()
        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')

        if not sender_id or not message_body:
            return Response(
                {"error": "sender_id and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        sender = User.objects.get(user_id=sender_id)
        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -----------------------
# Message ViewSet
# -----------------------
class MessageViewSet(viewsets.ModelViewSet):
    """
    Provides endpoints to list messages and create new messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['conversation', 'sender']
    search_fields = ['message_body']
    ordering_fields = ['sent_at']
