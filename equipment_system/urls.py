from django.urls import path
from . import views
app_name = 'equipment_system'
urlpatterns = [
    path('equipment/search', views.EquipmentSearchView.as_view(),
         name="equipment_search"),
]
