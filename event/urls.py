from django.urls import path
from . import views



app_name = 'event'


urlpatterns = [
    path('trigger/<int:user_id>/', views.trigger, name='alarm'),

]
