from django.urls import path
from . import views
app_name = 'service_system'
urlpatterns = [
    path('service_in/category', views.ServiceInCategoryListView.as_view(),
         name="service_in_category"),
    path('service_in/category/<int:category>',
         views.ServiceInCategoryListView.as_view(),
         name="service_in_category"),
    path('category_service/create', views.CategoryServiceCreateView.as_view(),
         name="category_service_create"),
    path('category_service/<int:pk>/delete',
         views.CategoryServiceDeleteView.as_view(),
         name="category_service_delete"),
    path('service/create', views.ServiceCreateView.as_view(),
         name="service_create"),
    path('<int:category>/service/create', views.ServiceCreateView.as_view(),
         name="service_create"),
    path('service/<int:pk>/update', views.ServiceUpdateView.as_view(),
         name="service_update"),
    path('service/<int:pk>/delete', views.ServiceDeleteView.as_view(),
         name="service_delete"),
    path('service/search', views.ServiceSearchView.as_view(),
         name="service_search"),
    path('covered/service', views.CoveredServiceApiView.as_view(),
         name="covered_service"),

]
