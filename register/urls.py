from django.urls import path
from . import views
app_name = 'register'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    # Пользователи
    path('user/<int:pk>/resource/', views.UserResourceView.as_view(),
         name="user_resource"),
    path('users/<int:func_structure>/resource/',
         views.UsersResourceView.as_view(), name="users_resource"),
    path('user/<int:pk>/events', views.UserEventsView.as_view(),
         name="user_events"),
    path('users/<int:func_structure>/events', views.UsersEventsView.as_view(),
         name="events_users"),
    # Ресурсы (оборудование)
    path('equipment/<int:pk>/resource/', views.EquipmentResourceView.as_view(),
         name="equipment_resource"),
    path('equipments/<int:equipment_group>/resource/', views.EquipmentsResourceView.as_view(),
         name="equipments_resource"),
    path('equipment/<int:pk>/events', views.EquipmentEventsView.as_view(),
         name="equipment_events"),
    path('equipments/<int:equipment_group>/events', views.EquipmentsEventsView.as_view(),
         name="equipments_events"),
    path('schedule/create/', views.ScheduleCreateView.as_view(),
         name="schedule_create"),
    path('schedule/<int:pk>/update', views.ScheduleUpdateView.as_view(),
         name="schedule_update"),
    path('free/slots', views.FreeSlotsView.as_view(),
         name="free_slots"),
    path('schedule/timer/<int:pk>/update',
         views.ScheduleTimerUpdateView.as_view(),
         name="schedule_timer_update"),
    path('schedule/timer/<int:pk>/delete',
         views.ScheduleDeleteView.as_view(),
         name="schedule_delete"),
    
]
