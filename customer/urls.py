from django.urls import path
from . import views
app_name = 'customer'
urlpatterns = [
    path('search/', views.CustomerSearchView.as_view(),
         name="search"),
    path('api/search/', views.CustomerApiSearchView.as_view(),
         name="api_search"),
    path('update/<int:pk>', views.CustomerUpdateView.as_view(),
         name="update"),
    path('create/', views.CustomerCreateView.as_view(),
         name="create"),
    path('detail/<int:pk>/', views.CustomerDetailView.as_view(),
         name="detail"),
    path('data/<int:pk>/', views.CustomerDataView.as_view(),
         name="data"),
]
