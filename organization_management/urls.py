from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/', include('account.urls', namespace='account')),
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls', namespace='customer')),
    path('register/', include('register.urls', namespace='register')),
    path('api/register/', include('register.api.urls', namespace='register_api')),
    path('work_time/', include('work_time.urls', namespace='work_time')),
    path('warehouse/', include('warehouse.urls', namespace='warehouse')),
    path('inspection/', include('inspection.urls', namespace='inspection')),
    path('equipment/system/', include('equipment_system.urls',
                                      namespace='equipment_system')),
    path('service/system/', include('service_system.urls',
                                    namespace='service')),
    path('document/circulation/', include('document_circulation.urls',
                                          namespace='document_circulation')),
    path('technological_card/', include('technological_card.urls',
                                        namespace='technological_card')),
    path('cashier/', include('cashier.urls', namespace='cashier')),
    path('internat_class_diseases/', include(
        'internat_class_diseases.urls', namespace='internat_class_diseases')),
    path('setting/', TemplateView.as_view(template_name="setting/index.html"),
         name='setting'),
    path('analytics/', include('analytics.urls', namespace='analytics')),
    path('import_data/', include('import_data.urls', namespace='import_data')),
]
