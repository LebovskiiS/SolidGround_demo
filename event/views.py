from importlib import reload

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from event.models import Alarm, AlarmResult, AlarmScenario
from main.models import UserInfo, Therapist, EmergencyContact, MusicTrack
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from event.models import AlarmScenario, Alarm, AlarmResult
from .utils import Notification


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trigger_alarm(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_info = UserInfo.objects.get(user=user)
    except (User.DoesNotExist, UserInfo.DoesNotExist):
        return Response({'error': 'User or UserInfo not found'}, status=404)

    scenario = user_info.scenario
    if not scenario:
        return Response({'error': 'No AlarmScenario associated with this user'}, status=404)


    response_data = {
        "scenario": scenario.name,
        "messages": []
    }


    if scenario.play_music and user_info.preferred_music:
        music_url = user_info.preferred_music.file_url
        response_data["messages"].append({"music_url":music_url})
    else:
        response_data["messages"].append("Музыка не воспроизводилась.")





    if scenario.notify_contact and user_info.emergency_contact:
        emergency_id = user_info.emergency_contact
        emergency_contact = EmergencyContact.objects.get(id=emergency_id)

        name = emergency_contact.name,
        relationship = emergency_contact.relationship
        phone = emergency_contact.phone
        email = emergency_contact.email

            
        notification = Notification(user_info.location, str(name),"Экстренная ситуация, требуется ваша помощь!", {":phone:": phone, ":email": email})
        notification.send_notification()

        response_data["messages"].append(f"Ваш/ваша{relationship} получил(а) уведомление.")
    else:
        response_data["messages"].append("Экстренные контакты не были уведомлены.")

    if scenario.notify_therapist and user_info.therapist_contact:
        therapist_contact = user_info.therapist_contact

        therapist_name = therapist_contact.name or "не указано"
        therapist_phone = therapist_contact.phone or "не указан"
        therapist_email = therapist_contact.email or "не указан"


        notification = Notification(
            user_info.location,
            therapist_name,
            "Экстренная ситуация, пользователь сообщает о необходимости связи.",
            {
                ":phone:": therapist_phone,
                ":email:": therapist_email
            }
        )
        notification.send_notification()


        response_data["messages"].append(f"Ваш психотерапевт ({therapist_name}) был уведомлён.")
    else:
        response_data["messages"].append("Психотерапевт не был уведомлён.")



    return Response(response_data, status=200)
