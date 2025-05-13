from django.urls import path
from . import views

appname = 'main'

urlpatterns = [
    path('register/', views.register, name='example_view'),  # Пример маршрута
]
