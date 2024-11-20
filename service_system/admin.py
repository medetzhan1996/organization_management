from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import CategoryService, Service, FormService


class ServiceResource(resources.ModelResource):

    class Meta:
        model = Service


class ServiceAdmin(ImportExportModelAdmin):
    resource_class = ServiceResource


class CategoryServiceResource(resources.ModelResource):

    class Meta:
        model = CategoryService


class CategoryServiceAdmin(ImportExportModelAdmin):
    resource_class = CategoryServiceResource


admin.site.register(CategoryService, CategoryServiceAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(FormService)
