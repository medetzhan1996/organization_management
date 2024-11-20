# urls.py
from django.urls import path
from register.api.views import FreeSlotsForSpecializationsInDateRangeView, ScheduleCreateView

app_name = 'register_api'
urlpatterns = [
    # ... другие URL-пути ...
    path('free_slots/', FreeSlotsForSpecializationsInDateRangeView.as_view(), name='specialization_free_slots_range'),
    path('schedule_create/', ScheduleCreateView.as_view(), name='schedule_create'),
]