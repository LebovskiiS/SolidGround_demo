from django.urls import path
from . import views



appname = 'event'


urlpatterns = [
    path('alarm/<id: user_id>', views.alarm, name='alarm'),
]