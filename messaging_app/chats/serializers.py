from rest_framework import serializers
from .models import User, Conversation, Message


# -----------------------
# User Serializer
# -----------------------
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'full_name',
            'email', 'phone_number', 'role', 'created_at'
        ]

    def get_full_name(self, obj):
        """Combine first_name and last_name into full_name"""
        return f"{obj.first_name} {obj.last_name}"


# -----------------------
# Message Serializer
# -----------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField(max_length=1000)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

    def validate_message_body(self, value):
        """Ensure message_body is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty")
        return value


# -----------------------
# Conversation Serializer
# -----------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'messages',
            'latest_message', 'created_at'
        ]

    def get_latest_message(self, obj):
        """Return the latest message body if messages exist"""
        latest = obj.messages.order_by('-sent_at').first()
        if latest:
            return latest.message_body
        return None
