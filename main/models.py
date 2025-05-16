from django.db import models
from django.contrib.auth.models import User
from event.models import AlarmScenario



class MusicTrack(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f"{self.name} track"


class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='therapist_profile')
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"Therapist {self.user.username}"



class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    age = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    military_status = models.BooleanField(default=False)
    ptsd_level = models.PositiveIntegerField(blank=True, null=True)
    preferred_music = models.ForeignKey(
        MusicTrack, on_delete=models.CASCADE, null=True, blank=True, related_name='preferred_by_users'
    )
    emergency_contact = models.OneToOneField(
        'EmergencyContact', on_delete=models.CASCADE, null=True, blank=True, related_name='user_info'
    )
    therapist_contact = models.ForeignKey(
        Therapist, on_delete=models.CASCADE, null=True, blank=True, related_name="users"
    )
    scenario = models.ForeignKey(
        AlarmScenario, on_delete=models.SET_NULL, null=True, blank=True, related_name='users', default=1
    )

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




class EmergencyContact(models.Model):
    name = models.CharField(max_length=100, blank=True)
    relationship = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"Emergency Contact: {self.name} ({self.relationship})"
