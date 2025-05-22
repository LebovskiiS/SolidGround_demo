from django.contrib import admin
from main import models as m_models
from event import models as e_models

admin.site.site_header = "My Blog Administration"
admin.site.register(m_models.UserInfo)
admin.site.register(e_models.AlarmScenario)
admin.site.register(e_models.Alarm)
admin.site.register(e_models.AlarmResult)