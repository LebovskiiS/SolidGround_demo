from django.urls import path
from .views import *




appname = 'main'

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login/', login, name='login'),
    path('edit/<int:user_id>/', edit_userinfo, name='edit_userinfo'),
    path('<int:user_id>/', get_userinfo, name='user'),

    path('edit/contact/<int:user_id>/', edit_emergency_contact, name ='edit_emergency_contact'),
    ]
