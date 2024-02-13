from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Storage, CategoryGood, Good,\
    StorageOperation, StorageOperationGood


class StorageResource(resources.ModelResource):

    class Meta:
        model = Storage


class StorageAdmin(ImportExportModelAdmin):
    resource_class = StorageResource


class CategoryGoodResource(resources.ModelResource):

    class Meta:
        model = CategoryGood


class CategoryGoodAdmin(ImportExportModelAdmin):
    resource_class = CategoryGoodResource


class GoodResource(resources.ModelResource):

    class Meta:
        model = Good


class GoodAdmin(ImportExportModelAdmin):
    resource_class = GoodResource


class StorageOperationResource(resources.ModelResource):

    class Meta:
        model = StorageOperation


class StorageOperationAdmin(ImportExportModelAdmin):
    resource_class = StorageOperationResource


class StorageOperationGoodResource(resources.ModelResource):

    class Meta:
        model = StorageOperationGood


class StorageOperationGoodAdmin(ImportExportModelAdmin):
    resource_class = StorageOperationGoodResource


admin.site.register(Storage, StorageAdmin)
admin.site.register(CategoryGood, CategoryGoodAdmin)
admin.site.register(Good, GoodAdmin)
admin.site.register(StorageOperation, StorageOperationAdmin)
admin.site.register(StorageOperationGood, StorageOperationGoodAdmin)
