from .gpt import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.shortcuts import render



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
def chat_view(request):
    if request.user.is_authenticated:
        websocket_url = 'ws://127.0.0.1:8000/ws/chat/global/'  # WebSocket маршрут для всех
        # Check both authentication and username for admin
        is_admin = request.user.is_authenticated and request.user.username == 'admin'
        return Response({
            'is_admin': is_admin,
            'websocket_url': websocket_url
        })
    return Response({'error': 'User not authenticated'}, status=403)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def support_chat_view(request, user_id):
    # Check both authentication and username for admin
    is_admin = request.user.is_authenticated and request.user.username == 'admin'

    if request.user.id != user_id and not is_admin:
        return Response({'error': 'You are not authorized to access this chat'}, status=403)

    try:
        user = User.objects.get(id=user_id)

        websocket_url = f'ws://127.0.0.1:8000/ws/chat/{user_id}/'
        return Response({
            'user_id': user_id,
            'is_admin': is_admin,
            'websocket_url': websocket_url
        })

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)




@api_view(['GET'])
@permission_classes([])
def my_dynamic_view(request):
    MyModel = get_model_class("app_name", "ModelName")
    data = MyModel.objects.all().values()  # Используем загруженную модель
    return Response(data)
