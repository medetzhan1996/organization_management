from django.urls import path
from . import views
app_name = 'inspection'
urlpatterns = [
    path('reception_with_action/list/',
         views.ReceptionWithActionListView.as_view(),
         name="reception_with_action_list"),
    path('reception/list/', views.ReceptionListView.as_view(),
         name="reception_list"),
]
