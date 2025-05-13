from django.contrib import admin
from main import models


admin.site.site_header = "My Blog Administration"
admin.site.register(models.UserInfo)
admin.site.register(models.ChatMessage)
admin.site.register(models.ChatSession)
admin.site.register(models.SignalSession)