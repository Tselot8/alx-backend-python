from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = [IsParticipantOfConversation]
    lookup_field = 'conversation_id'

    def get_queryset(self):
        # Only filter for list/retrieve, not for custom actions like add_message
        if self.action in ['list', 'retrieve']:
            return self.queryset.filter(participants=self.request.user)
        return self.queryset
    
    @action(detail=True, methods=['post'])
    def add_message(self, request, conversation_id=None):
        conversation = self.get_object()  # DRF will fetch the conversation by the router lookup
        message_body = request.data.get('message_body')

        if not message_body or not message_body.strip():
            return Response({"error": "message_body is required."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant of this conversation."}, status=status.HTTP_403_FORBIDDEN)

        try:
            message = Message.objects.create(
                sender=request.user,
                conversation=conversation,
                message_body=message_body
            )
        except IntegrityError:
            return Response({"error": "Failed to create message."}, status=status.HTTP_400_BAD_REQUEST)

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
    filterset_class = MessageFilter        
    search_fields = ['message_body']
    ordering_fields = ['sent_at']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination

    def get_queryset(self):
        # Return only messages in conversations the user participates in, ordered by sent_at
        return Message.objects.filter(conversation__participants=self.request.user).order_by('sent_at')

    def perform_create(self, serializer):
        # Automatically set the sender to the current user
        serializer.save(sender=self.request.user)
    
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not username or not password or not email:
            return Response(
                {"error": "username, password, and email are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError:
            return Response({"error": "Username or email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    
@api_view(["POST"])
def test_admin_action(request):
    return Response({"success": "Admin action performed!"})
