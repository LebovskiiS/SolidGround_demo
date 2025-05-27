from django.db import models
from django.contrib.auth.models import User


class ChatSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_sessions'
    )
    session_type = models.CharField(
        max_length=10,
        choices=[
            ('gpt', 'GPT'),  # Chat with GPT
            ('user', 'User')  # Chat with a real person
        ],
        default='gpt',  # Default chat with GPT
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_chats',
        help_text="Indicates a real user (if not chatting with GPT)."
    )
    started_at = models.DateTimeField(auto_now_add=True)  # Chat start time
    ended_at = models.DateTimeField(null=True, blank=True)  # Chat end time, if completed

    def __str__(self):
        if self.session_type == 'gpt':
            return f"Chat with GPT by {self.user.username} at {self.started_at}"
        return f"Chat with {self.receiver.username} by {self.user.username} at {self.started_at}"


class ChatMessage(models.Model):
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.CharField(
        max_length=10,
        choices=[
            ('user', 'User'),
            ('gpt', 'GPT'),
            ('system', 'System')
        ],
        help_text="Who sent the message."
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.upper()} at {self.timestamp}"
