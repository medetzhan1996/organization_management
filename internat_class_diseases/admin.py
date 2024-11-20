from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import MKB10, Conclusion


class MKB10Resource(resources.ModelResource):

    class Meta:
        model = MKB10


class MKB10Admin(ImportExportModelAdmin):
    resource_class = MKB10Resource


admin.site.register(MKB10, MKB10Admin)
admin.site.register(Conclusion)