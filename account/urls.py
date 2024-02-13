from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('identify/role', views.IdentifyRole.as_view(), name='identify_role'),
    path('user/priority/', views.UserPriorityView.as_view(),
         name="user_priority"),
    path('equipment/priority/', views.EquipmentPriorityView.as_view(),
         name="equipment_priority"),
]
