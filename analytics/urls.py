from django.urls import path
from . import views
app_name = 'analytics'
urlpatterns = [
    path('record', views.RecordView.as_view(), name="record"),
    path('speciality', views.SpecialityView.as_view(), name="speciality"),
    path('doctor', views.DoctorView.as_view(), name="doctor"),
    path('customer', views.CustomerView.as_view(), name="customer"),
    path('customer/<int:pk>', views.CustomerView.as_view(), name="customer"),
    path('visit', views.VisitView.as_view(), name="visit"),
]
