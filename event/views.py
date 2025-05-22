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
def trigger(request, user_id):
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


    if scenario.play_music and user_info.music:
        music_url = user_info.music.url
        response_data["messages"].append({"music_url":music_url})
    else:
        response_data["messages"].append("Музыка не воспроизводилась.")

    if scenario.notify_contact and user_info.user.emergency_contacts.exists():
        emergency_contacts = user_info.user.emergency_contacts.all()

        for emergency_contact in emergency_contacts:
            name = emergency_contact.name
            relationship = emergency_contact.relationship
            phone = emergency_contact.phone
            email = emergency_contact.email


            notification = Notification(
                location=user_info.location,
                name=name,
                message="Экстренная ситуация, требуется ваша помощь!",
                contact={":phone:": phone, ":email": email},
                user_name=user_info.user.username
            )


            email_result = notification.send_email(
                recipient_email=email,
                user_name=user_info.user.username,
            )

            if email_result.get("status") == "success":
                response_data["messages"].append(
                    f"Ваш/ваша {relationship} ({name}) получил(а) уведомление по email."
                )
            else:
                response_data["messages"].append(
                    f"Ошибка отправки уведомления для {relationship} ({name}): {email_result.get('message')}"
                )
    else:
        response_data["messages"].append("Экстренные контакты не были уведомлены.")




    if scenario.notify_therapist and user_info.therapist_contact:
        therapist_contact = user_info.therapist_contact

        therapist_name = therapist_contact.name or "не указано"
        therapist_phone = therapist_contact.phone or "не указан"
        therapist_email = therapist_contact.email or "не указан"

        notification = Notification(
            location=user_info.location,
            name=therapist_name,
            message="Экстренная ситуация, пользователь сообщает о необходимости связи.",
            contact={
                ":phone:": therapist_phone,
                ":email:": therapist_email
            }
        )

        notification.send_email(
            recipient_email=therapist_email,
            user_name=therapist_name,
            message_text=None
        )

        response_data["messages"].append(f"Ваш психотерапевт ({therapist_name}) был уведомлён.")
    else:
        response_data["messages"].append("Психотерапевт не был уведомлён.")

    return Response(response_data, status=200)
