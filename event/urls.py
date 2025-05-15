from django.urls import path
from . import views



appname = 'event'


urlpatterns = [
    path('triger/<int:user_id>/', views.trigger_alarm, name='alarm'),

]