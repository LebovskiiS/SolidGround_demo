from django.urls import path
from . import views




appname = 'main'

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('edit/user/<int:user_id>/', views.edit_userinfo, name='edit_userinfo'),

    path('userinfo/<int:user_id>/', views.get_userinfo, name='userinfo'),

    path('user/<int:user_id>/', views.get_userinfo, name='user'),
]
