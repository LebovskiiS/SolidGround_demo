
from DjangoProject.settings import ALARM_MESSAGE_TO_SEND_1, ALARM_MESSAGE_TO_SEND_2, DEFAULT_SUBJECT_EMAIL



class Notification:
    def __init__(self, location: str = None, name: str = None, message: str = None, contact: dict[str, str] = None,
                 message_text: str = None, user_name: str = None):

        self.location = location if location else "Не предоставлено"
        self.name = name
        self.message = message
        self.contact = contact
        self.message_text = message_text
        self.user_name = user_name

    def send_email(self, recipient_email: str, user_name: str, message_text: str = None, subject: str = "title",
                   location: str = None):

        location = location if location else self.location
        subject = f"Привет, {user_name}!" if subject == "title" else subject

        if not message_text:

            full_message = f'{ALARM_MESSAGE_TO_SEND_1} {user_name}, {ALARM_MESSAGE_TO_SEND_2}, Локация: {location}'

        else:
            full_message = message_text

        try:
            from django.core.mail import send_mail
            from django.conf import settings

            send_mail(
                subject=subject,
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False,
            )
            return {"status": "success",
                    "message": f"Email has been sent to {recipient_email} location: {location}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}



    def send_whatsapp(self):
        pass
