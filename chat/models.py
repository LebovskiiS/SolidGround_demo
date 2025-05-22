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
            ('gpt', 'GPT'),  # Чат с GPT
            ('user', 'User')  # Чат с реальным человеком
        ],
        default='gpt',  # По умолчанию чат с GPT
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_chats',
        help_text="Указывает реального пользователя (если чат не с GPT)."
    )
    started_at = models.DateTimeField(auto_now_add=True)  # Время начала чата
    ended_at = models.DateTimeField(null=True, blank=True)  # Время завершения чата, если завершен

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
        help_text="Кто отправил сообщение."
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.upper()} at {self.timestamp}"