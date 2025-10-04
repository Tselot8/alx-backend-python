# messaging/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from .models import Message
from .managers import UnreadMessagesManager

# ---- Delete user ----
@login_required
def delete_user(request):
    """
    Allow the logged-in user to delete their account.
    Triggers post_delete signals to clean up related data.
    """
    user = request.user
    user.delete()
    return redirect("/")  # Redirect to home or login page

# ---- Inbox view with unread messages and caching ----
@cache_page(60)  # cache the view for 60 seconds
@login_required
def inbox(request):
    """
    Display unread messages for the current user,
    optimized with select_related, prefetch_related, and .only().
    """
    messages = Message.unread.unread_for_user(request.user)
    
    return render(request, "message/inbox.html", {"messages": messages})

# ---- Recursive function to fetch all replies in threaded format ----
def get_all_replies(message):
    """
    Recursively fetch all replies for a given message,
    optimized with select_related and only() to reduce queries.
    """
    replies_list = []
    for reply in message.replies.all().select_related('sender', 'receiver')\
            .only('id', 'sender', 'receiver', 'content', 'timestamp', 'parent_message'):
        replies_list.append({
            "reply": reply,
            "replies": get_all_replies(reply)  # recursive call
        })
    return replies_list

# ---- Threaded conversation view ----
@login_required
def threaded_conversation(request, message_id):
    """
    Display a message and all of its replies in a threaded format.
    """
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').prefetch_related('replies')\
            .only('id', 'sender', 'receiver', 'content', 'timestamp', 'parent_message'),
        pk=message_id
    )
    
    threaded_replies = get_all_replies(message)
    
    return render(request, "message/threaded.html", {
        "message": message,
        "threaded_replies": threaded_replies
    })
