from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Customer


class CustomerResource(resources.ModelResource):

    class Meta:
        model = Customer


class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource


admin.site.register(Customer, CustomerAdmin)
