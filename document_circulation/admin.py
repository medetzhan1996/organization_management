from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Form, Row, Marker, GroupForm, CompanyForm,\
    FuncStructureForm, FormHistory, ReadyPhrase, AdaptiveMarker


def form_detail(obj):
    url = reverse('document_circulation:admin_form_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


class FormResource(resources.ModelResource):

    class Meta:
        model = Form


class FormAdmin(ImportExportModelAdmin):
    resource_class = FormResource
    list_display = ('title', form_detail, )
    search_fields = ('title', )


class RowResource(resources.ModelResource):

    class Meta:
        model = Row


class RowAdmin(ImportExportModelAdmin):
    resource_class = RowResource


class MarkerResource(resources.ModelResource):

    class Meta:
        model = Marker


class MarkerAdmin(ImportExportModelAdmin):
    resource_class = MarkerResource
    search_fields = ('name', 'row__id', )


class GroupFormResource(resources.ModelResource):

    class Meta:
        model = GroupForm


class GroupFormAdmin(ImportExportModelAdmin):
    resource_class = GroupFormResource


class CompanyFormResource(resources.ModelResource):

    class Meta:
        model = CompanyForm


class CompanyFormAdmin(ImportExportModelAdmin):
    resource_class = CompanyFormResource


class FuncStructureFormResource(resources.ModelResource):

    class Meta:
        model = FuncStructureForm


class FuncStructureFormAdmin(ImportExportModelAdmin):
    resource_class = FuncStructureFormResource


class FormHistoryResource(resources.ModelResource):

    class Meta:
        model = FormHistory


class FormHistoryAdmin(ImportExportModelAdmin):
    resource_class = FormHistoryResource


class ReadyPhraseResource(resources.ModelResource):

    class Meta:
        model = ReadyPhrase


class ReadyPhraseAdmin(ImportExportModelAdmin):
    resource_class = ReadyPhraseResource


class AdaptiveMarkerResource(resources.ModelResource):

    class Meta:
        model = AdaptiveMarker


class AdaptiveMarkerAdmin(ImportExportModelAdmin):
    resource_class = AdaptiveMarkerResource


admin.site.register(Form, FormAdmin)
admin.site.register(Row, RowAdmin)
admin.site.register(Marker, MarkerAdmin)
admin.site.register(GroupForm, GroupFormAdmin)
admin.site.register(CompanyForm, CompanyFormAdmin)
admin.site.register(FuncStructureForm, FuncStructureFormAdmin)
admin.site.register(FormHistory, FormHistoryAdmin)
admin.site.register(ReadyPhrase, ReadyPhraseAdmin)
admin.site.register(AdaptiveMarker, AdaptiveMarkerAdmin)
