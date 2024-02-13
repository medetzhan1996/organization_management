from django.contrib import admin
from .models import WorkTime, WorkTimeExclusion

admin.site.register(WorkTime)
admin.site.register(WorkTimeExclusion)
