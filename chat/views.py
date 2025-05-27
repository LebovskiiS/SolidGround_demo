from .gpt import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_get_message_gpt(request, user_id):
    if request.user.id != user_id:
        return Response({'error': 'You are not authorized to send messages to this user'}, status=403)
    try:
        user = User.objects.get(id=user_id)
        text = request.data.get('text')
        if not text:
            return Response({'error': 'Message text is required'}, status=400)
        gpt = GPT(user.id)
        response = gpt.get_response(text)
        return Response({'response': response}, status=200)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message_to_user(request, session_id):
    try:
        chat_session = ChatSession.objects.get(id=session_id)

        if request.user != chat_session.user and request.user != chat_session.receiver:
            return Response({'error': 'You are not authorized for this chat session'}, status=403)

        text = request.data.get('text')
        if not text:
            return Response({'error': 'Message text is required'}, status=400)

        sender_type = 'user' if request.user == chat_session.user else 'system'
        message = ChatMessage.objects.create(
            session=chat_session,
            sender=sender_type,
            message=text
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat_session.id}",
            {
                "type": "chat.message",
                "message": {
                    "id": message.id,
                    "sender": message.sender,
                    "text": message.message,
                    "timestamp": message.timestamp.isoformat(),
                }
            }
        )

        return Response({'message': 'Message sent successfully'})

    except ChatSession.DoesNotExist:
        return Response({'error': 'Chat session does not exist'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
