from django.urls import path
from . import views



appname = 'event'


urlpatterns = [
    path('trigger/<int:user_id>/', views.trigger, name='alarm'),

]