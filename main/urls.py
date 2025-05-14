from django.urls import path
from . import views




appname = 'main'

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('edit_userinfo/', views.edit_userinfo, name='edit_userinfo'),

    path('user/<int:user_id>/', views.get_userinfo, name='user'),
]
