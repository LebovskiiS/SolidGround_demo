from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    age = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    military_status = models.CharField(max_length=100, blank=True)
    ptsd_level = models.CharField(max_length=100, blank=True)
    preferred_music = models.CharField(max_length=200, blank=True)
    emergency_contacts = models.TextField(blank=True)  # JSON или просто список
    therapist_contact = models.CharField(max_length=100, blank=True)  # e-mail, тел. и т.п.

    def __str__(self):
        return f"Profile for {self.user.username}"



class SignalSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signal_sessions')
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True)
    music_played = models.BooleanField(default=False)
    message_sent_to_contacts = models.BooleanField(default=False)
    voice_message_played = models.BooleanField(default=False)
    therapist_notified = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"SignalSession {self.id} for {self.user.username}"



class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_limit_minutes = models.IntegerField(default=10)

    def __str__(self):
        return f"ChatSession {self.id} for {self.user.username}"



class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('gpt', 'GPT')])
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.upper()} at {self.timestamp}"
