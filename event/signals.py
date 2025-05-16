from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import AlarmScenario


@receiver(post_migrate)
def create_alarm_scenarios(sender, **kwargs):
    scenarios = [
        (1, 'Off', False, False, False),  # id, name, play_music, notify_contact, notify_therapist
        (2, 'Pattern 1', True, False, False),
        (3, 'Pattern 2', True, True, True),
        (4, 'Pattern 3', True, False, True),
    ]

    for id, name, play_music, notify_contact, notify_therapist in scenarios:
        if not AlarmScenario.objects.filter(id=id).exists():
            AlarmScenario.objects.create(
                id=id,
                name=name,
                play_music=play_music,
                notify_contact=notify_contact,
                notify_therapist=notify_therapist
            )

