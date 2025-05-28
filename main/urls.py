from django.urls import path
from .views import *




app_name = 'main'

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login/', login, name='login'),
    path('edit/<int:user_id>/', edit_userinfo, name='edit_userinfo'),
    path('<int:user_id>/', get_userinfo, name='user'),

    path('edit/contact/<int:user_id>/', edit_emergency_contact, name ='edit_emergency_contact'),
    # path('music/', get_music, name= 'get_music'),
    # path('music/edit/<int:user_id>/', set_music, name='set_music'),

    path('create/therapist/<int:user_id>/', create_therapist_contact, name='create_therapist_contact'),
    path('edit/therapist/<int:user_id>/', edit_therapist_contact, name='edit_therapist_contact'),
    ]
