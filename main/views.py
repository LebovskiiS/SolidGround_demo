from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, UserInfoSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from . import models
from django.db import transaction

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
@transaction.atomic
def registration(request ):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User Created"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
@transaction.atomic
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)




@api_view(['UPDATE'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def edit_userinfo(request):
    try:
        user_id = request.user.id
        data = request.data

        try:
            user_info = models.UserInfo.objects.get(user_id=user_id)
        except models.UserInfo.DoesNotExist:
            return Response({"error": "UserInfo not found for this user."}, status=status.HTTP_404_NOT_FOUND)


        user_info.age = data.get('age', user_info.age)  # Если age отсутствует, сохраняется текущее значение
        user_info.location = data.get('location', user_info.location)
        user_info.military_status = data.get('military_status', user_info.military_status)
        user_info.ptsd_level = data.get('ptsd_level', user_info.ptsd_level)
        user_info.preferred_music = data.get('preferred_music', user_info.preferred_music)
        user_info.emergency_contact = data.get('emergency_contact', user_info.emergency_contact)
        user_info.therapist_contact = data.get('therapist_contact', user_info.therapist_contact)
        user_info.save()

        return Response({"message": "User info updated successfully."}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_userinfo(request, user_id):
    try:
        user_info = models.UserInfo.objects.get(user_id=user_id)
    except models.UserInfo.DoesNotExist:
        return Response({"error": "UserInfo not found for this user."}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserInfoSerializer(user_info)
    return Response(serializer.data)




