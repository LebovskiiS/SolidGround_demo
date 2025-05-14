from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    age = models.IntegerField(null= True, blank= True)
    location = models.CharField(max_length= 100, blank= True)
    military_status = models.CharField(max_length= 100, blank= True)
    ptsd_level = models.IntegerField(blank= True, null= True)
    preferred_music = models.CharField(max_length= 200, blank=True)
    emergency_contacts = models.TextField(blank=True)
    therapist_contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"




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


class Therapist(models.Model):
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"Therapist {self.name}"



class MusicTrack(models.Model):
    name = models.CharField(max_length=100)
    file_url = models.URLField()

    def __str__(self):
        return f"{self.name} track"


class UserContact(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100, blank=True)
    relationship = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"Contact {self.name} ({self.user_info.user.username})"