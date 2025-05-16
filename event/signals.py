from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import AlarmScenario



@receiver(post_migrate)
def create_alarm_scenarios(sender, **kwargs):
    scenarios = [
        ('Off', False, False, False),  # name, play_music, notify_contact, notify_therapist
        ('Patten 1', True, False, False),
        ('Pattern 2', True, True, True),
        ('Pattern 3', True, False, True),
    ]

    for name, play_music, notify_contact, notify_therapist in scenarios:
        if not AlarmScenario.objects.filter(name=name).exists():
            AlarmScenario.objects.create(
                name=name,
                play_music=play_music,
                notify_contact=notify_contact,
                notify_therapist=notify_therapist
            )


