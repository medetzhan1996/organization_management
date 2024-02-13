from django.urls import path
from . import views
app_name = 'import_data'
urlpatterns = [
    path('form/', views.ImportFormView.as_view(),
         name="form"),
    path('mkb10/', views.ImportMkb10View.as_view(), name="mkb10"),
]
