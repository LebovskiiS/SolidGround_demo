from django.db import models
from django.contrib.auth.models import User



class AlarmScenario(models.Model):
    name = models.CharField(max_length=100)
    play_music = models.BooleanField(default=True)
    notify_contact = models.BooleanField(default=True)
    notify_therapist = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alarms')
    scenario = models.ForeignKey(AlarmScenario, on_delete=models.CASCADE, related_name='alarms')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alarm by {self.user.username} at {self.timestamp}"



class AlarmResult(models.Model):
    alarm = models.OneToOneField(Alarm, on_delete=models.CASCADE, related_name='session')
    location = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    music_played = models.BooleanField(default=False)
    message_sent_to_contacts = models.BooleanField(default=False)
    voice_message_played = models.BooleanField(default=False)
    therapist_notified = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"AlarmResult {self.id} for {self.alarm.user.username}"

