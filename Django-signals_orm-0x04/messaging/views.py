# messaging/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from .models import Message

# ---- Delete user ----
@login_required
def delete_user(request):
    user = request.user
    user.delete()  # triggers post_delete signals
    return redirect("/")

# ---- Inbox view with unread messages and caching ----
@cache_page(60)  # cache 60 seconds
@login_required
def inbox(request):
    # Fetch unread messages for the current user, optimized
    messages = Message.objects.filter(receiver=request.user, read=False)\
        .select_related('sender', 'receiver')\
        .prefetch_related('replies')\
        .only('id', 'sender', 'receiver', 'content', 'timestamp', 'read', 'parent_message')
    
    return render(request, "message/inbox.html", {"messages": messages})

# ---- Recursive function to fetch all replies in threaded format ----
def get_all_replies(message):
    replies_list = []
    for reply in message.replies.all().select_related('sender', 'receiver').only('id', 'sender', 'receiver', 'content', 'timestamp', 'parent_message'):
        replies_list.append({
            "reply": reply,
            "replies": get_all_replies(reply)  # recursive call
        })
    return replies_list

# ---- Threaded conversation view ----
@login_required
def threaded_conversation(request, message_id):
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').prefetch_related('replies').only(
            'id', 'sender', 'receiver', 'content', 'timestamp', 'parent_message'
        ),
        pk=message_id
    )
    
    threaded_replies = get_all_replies(message)
    
    return render(request, "message/threaded.html", {"message": message, "threaded_replies": threaded_replies})
