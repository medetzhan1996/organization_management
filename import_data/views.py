from django.shortcuts import render
from django.db import connections
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from document_circulation.models import Form, Row, Marker
from internat_class_diseases.models import MKB10


class ImportFormView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        with connections['db_03'].cursor() as cursor:
            cursor.execute("SELECT id, description FROM forms")
            forms = cursor.fetchall()
            for form in forms:
                form_id = form[0]
                if not Form.objects.filter(old_id=int(form_id)).exists():
                    form_obj = Form.objects.create(title=form[1], old_id=form_id)
                    cursor.execute(
                        "SELECT id, form_id, type, position FROM rows WHERE form_id = %s",
                        [form_id])
                    rows = cursor.fetchall()
                    for row in rows:
                        row_id = row[0]
                        row_obj = Row.objects.create(form=form_obj, kind=row[2], position=row[3])
                        cursor.execute(
                            "SELECT id, rowspan, name, label, type, colspan, options, is_bold, is_italic, is_center,"
                            "is_border, grouping, group_separator  FROM markers WHERE row_id = %s",
                            [row_id])
                        markers = cursor.fetchall()
                        for marker in markers:
                            is_bold = True if marker[7] else False
                            is_italic = True if marker[8] else False
                            is_center = True if marker[9] else False
                            is_border = True if marker[10] else False
                            marker_obj = Marker(
                                row=row_obj, name=marker[2], label=marker[3],
                                kind=marker[4], colspan=marker[5], is_bold=is_bold,
                                is_italic=is_italic, is_center=is_center, is_border=is_border,
                                grouping=marker[11], group_separator=marker[12],
                                rowspan=marker[1], options=marker[6]
                            )
                            marker_obj.save()
        return render(request, 'import_data/form.html')


class ImportMkb10View(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        MKB10.objects.all().delete()
        with connections['db_03'].cursor() as cursor:
            cursor.execute(
                "SELECT id, mkb_code, mkb_name, parent_id FROM mkb_10 WHERE parent_id = '-'")
            mkbs_0 = cursor.fetchall()
            for mkb_0 in mkbs_0:
                mkb_0_id = str(mkb_0[0])
                mkb_0_obj = MKB10.objects.create(title=mkb_0[2], code=mkb_0[1], parent=None)
                cursor.execute("SELECT id, mkb_code, mkb_name, parent_id FROM mkb_10 WHERE parent_id = %s",
                                        [mkb_0_id])
                mkbs_1 = cursor.fetchall()
                if mkbs_1:
                    for mkb_1 in mkbs_1:
                        mkb_1_id = str(mkb_1[0])
                        mkb_1_obj = MKB10.objects.create(title=mkb_1[2], code=mkb_1[1], parent=mkb_0_obj)
                        cursor.execute("SELECT id, mkb_code, mkb_name, parent_id FROM mkb_10 WHERE parent_id = %s",
                                                [mkb_1_id])
                        mkbs_2 = cursor.fetchall()
                        if mkbs_2:
                            for mkb_2 in mkbs_2:
                                mkb_2_id = str(mkb_2[0])
                                mkb_2_obj = MKB10.objects.create(title=mkb_2[2], code=mkb_2[1], parent=mkb_1_obj)
                                cursor.execute(
                                    "SELECT id, mkb_code, mkb_name, parent_id FROM mkb_10 WHERE parent_id = %s",
                                    [mkb_2_id])
                                mkbs_3 = cursor.fetchall()
                                for mkb_3 in mkbs_3:
                                    MKB10.objects.create(title=mkb_3[2], code=mkb_3[1], parent=mkb_2_obj)
        return render(request, 'import_data/form.html')
