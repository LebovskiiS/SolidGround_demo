from django.contrib.auth import authenticate
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import *
from django.db import transaction
from django.contrib.auth.models import User
from .exceptions import *


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




@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def edit_userinfo(request, user_id):
    try:
        data = request.data
        try:
            user_info = UserInfo.objects.get(user_id=user_id)
        except UserInfo.DoesNotExist:
            return Response({"error": "UserInfo not found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # Обновляем данные
        user_info.age = data.get('age', user_info.age)
        user_info.location = data.get('location', user_info.location)
        user_info.military_status = data.get('military_status', user_info.military_status)
        user_info.ptsd_level = data.get('ptsd_level', user_info.ptsd_level)
        user_info.therapist_contact = data.get('therapist_contact', user_info.therapist_contact)

        scenario_id = data.get('scenario')
        if scenario_id:
            try:
                scenario = AlarmScenario.objects.get(id=scenario_id)
                user_info.scenario = scenario
            except AlarmScenario.DoesNotExist:
                return Response({"error": "AlarmScenario not found with this id."}, status=status.HTTP_400_BAD_REQUEST)

        user_info.save()


        user_info_data = {
            "age": user_info.age,
            "location": user_info.location,
            "military_status": user_info.military_status,
            "ptsd_level": user_info.ptsd_level,
            "therapist_contact": user_info.therapist_contact.id if user_info.therapist_contact else None,
            "scenario": user_info.scenario.id if user_info.scenario else None,
        }

        return Response({
            "message": "UserInfo updated successfully.",
            "updated_data": user_info_data,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_userinfo(request, user_id):
    try:
        user_info = UserInfo.objects.get(user_id=user_id)
    except UserInfo.DoesNotExist:
        return Response({"error": "UserInfo not found for this user."}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserInfoSerializer(user_info)
    return Response(serializer.data)







@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_emergency_contact(request, user_id):
    try:
        if request.user.id != user_id:
            return Response(
                {"error": "You are not authorized to edit another user's emergency contact."},
                status=403
            )

        name = request.data.get("name")
        phone = request.data.get("phone")
        email = request.data.get("email")
        relationship = request.data.get("relationship")

        if not name or not phone or not relationship:
            return Response(
                {"error": "The 'name', 'phone', and 'relationship' fields are required."},
                status=400
            )


        emergency_contact = EmergencyContact.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            email=email,
            relationship=relationship
        )


        return Response({
            "message": "A new emergency contact has been created.",
            "data": {
                "id": emergency_contact.id,
                "name": emergency_contact.name,
                "phone": emergency_contact.phone,
                "email": emergency_contact.email,
                "relationship": emergency_contact.relationship,
            }
        }, status=201)

    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}"},
            status=400
        )




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_music(request, user_id):
    try:
        if request.user.id == user_id:
            request.user.preferred_music = request.data.get("music")
            request.user.save()
            return Response({"message": "Music track updated successfully"}, status=200)

        return Response(
            {"error": "You are not authorized to edit this user's music preferences."},
            status=403
        )

    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}"},
            status=400
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_music(request):
    try:
        tracks = MusicTrack.objects.all()
        response = MusicSerializer(tracks, many=True).data
        return Response(response, status=200)
    except Exception as e:
        raise ErrorNoRightForThisUser()

