from django.contrib import admin
from .models import Schedule, ScheduleService, ScheduleEquipment

admin.site.register(Schedule)
admin.site.register(ScheduleService)
admin.site.register(ScheduleEquipment)
