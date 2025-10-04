from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from .models import Message
from .managers import UnreadMessagesManager

# ---- Delete user ----
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect("/")

# ---- Inbox view with unread messages and caching ----
@cache_page(60)  # cache 60 seconds
@login_required
def inbox(request):
    messages = Message.unread.unread_for_user(request.user).select_related('sender', 'receiver').prefetch_related('replies')
    return render(request, "message/inbox.html", {"messages": messages})

# ---- Threaded conversation view ----
@login_required
def threaded_conversation(request, message_id):
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').prefetch_related('replies'),
        pk=message_id
    )
    replies = message.replies.all()  # already prefetched
    return render(request, "message/threaded.html", {"message": message, "replies": replies})
