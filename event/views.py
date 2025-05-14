from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from event.models import Alarm, AlarmResult, AlarmScenario
from main.models import UserInfo, Therapist, UserContact, MusicTrack
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trigger_alarm(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_info = UserInfo.objects.get(user=user)
    except (User.DoesNotExist, UserInfo.DoesNotExist):
        return Response({'error': 'User or UserInfo not found'}, status=404)

    # Получаем сценарий тревоги (например, последний или дефолтный)
    scenario = AlarmScenario.objects.first()  # Для простоты выбираем первый сценарий

    # Создаём запись о тревоге
    alarm = Alarm.objects.create(user=user, scenario=scenario)

    # Инициализируем переменные результата
    music_played = False
    contacts_notified = False
    voice_played = False
    therapist_notified = False
    music_url = None

    # === Выполняем сценарий ===
    if scenario.play_music and user_info.preferred_music:
        music_played = True
        music_url = user_info.preferred_music.file_url

    if scenario.notify_contacts and user_info.contacts.exists():
        contacts_notified = True
        # Здесь может быть отправка SMS или email

    if scenario.notify_therapist and user_info.therapist:
        therapist_notified = True
        # Здесь может быть логика уведомления терапевта

    # Сохраняем результат тревоги
    alarm_result = AlarmResult.objects.create(
        alarm=alarm,
        location=request.data.get('location', ''),
        music_played=music_played,
        message_sent_to_contacts=contacts_notified,
        voice_message_played=voice_played,
        therapist_notified=therapist_notified,
        completed=True
    )


    return Response({
        'alarm_id': alarm.id,
        'scenario': scenario.name,
        'result': {
            'music_played': music_played,
            'music_url': music_url,
            'contacts_notified': contacts_notified,
            'therapist_notified': therapist_notified,
            'completed': True
        }
    }, status=201)