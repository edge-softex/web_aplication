from django.contrib import admin

from .models import PVData, PowerForecast, YieldDay, YieldMonth, YieldYear, YieldMinute, Settings, Log, AIAlgorithm

# Register your models here.

admin.site.register(PVData)
admin.site.register(PowerForecast)
admin.site.register(YieldDay)
admin.site.register(YieldMonth)
admin.site.register(YieldYear)
admin.site.register(YieldMinute)
admin.site.register(Settings)
admin.site.register(Log)
admin.site.register(AIAlgorithm)