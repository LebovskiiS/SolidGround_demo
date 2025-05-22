from .gpt import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User





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
def send_message_to_user(request, user_id):
    if request.user.id != user_id:
        return Response({'error': 'You are not authorized to send messages from this user_id'}, status=403)
    try:
        user = User.objects.get(id=user_id)
        text = request.data.get('text')
        if not text:
            return Response({'error': 'Message text is required'}, status=400)
        gpt = GPT(user.id)
        response = gpt.send_message(text)
