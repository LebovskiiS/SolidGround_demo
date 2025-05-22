
# from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from .settings import API_VERSION

urlpatterns = [
       path('admin/', admin.site.urls),
       path(f'api/{API_VERSION}/user/', include('main.urls')),
       path(f'api/{API_VERSION}/event/', include('event.urls'))
       path(f'api/{API_VERSION}/chat/', include('chat.urls')),
]
