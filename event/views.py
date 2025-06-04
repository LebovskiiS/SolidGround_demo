from main.models import UserInfo

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
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


    # Music functionality moved to frontend
    if scenario.play_music:
        response_data["play_music"] = True
    else:
        response_data["play_music"] = False
        response_data["messages"].append("Music was not played.")

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
                message="Emergency situation, your help is needed!",
                contact={":phone:": phone, ":email:": email},
                user_name=user_info.user.username
            )


            email_result = notification.send_email(
                recipient_email=email,
                user_name=user_info.user.username,
            )

            if email_result.get("status") == "success":
                response_data["messages"].append(
                    f"Your {relationship} ({name}) received a notification by email."
                )
            else:
                response_data["messages"].append(
                    f"Error sending notification to {relationship} ({name}): {email_result.get('message')}"
                )
    else:
        response_data["messages"].append("Emergency contacts were not notified.")




    if scenario.notify_therapist and user_info.therapist_contact:
        therapist_contact = user_info.therapist_contact

        therapist_name = therapist_contact.name or "not specified"
        therapist_phone = therapist_contact.phone or "not specified"
        therapist_email = therapist_contact.email or "not specified"

        notification = Notification(
            location=user_info.location,
            name=therapist_name,
            message="Emergency situation, user reports the need for communication.",
            contact={
                ":phone:": therapist_phone,
                ":email:": therapist_email
            },
            user_name=user_info.user.username
        )

        notification.send_email(
            recipient_email=therapist_email,
            user_name=therapist_name,
            message_text=None
        )

        response_data["messages"].append(f"Your therapist ({therapist_name}) was notified.")
    else:
        response_data["messages"].append("Therapist was not notified.")

    return Response(response_data, status=200)
