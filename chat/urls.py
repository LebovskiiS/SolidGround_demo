from django.urls import path
from . import views


appname = 'chat'


urlpatterns = [
    path('/<int:user_id>/', views. send_get_message_gpt, name= 'send_get_message')
]