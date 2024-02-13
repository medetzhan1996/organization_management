import json
from django.db import models
from django.conf import settings
from django.db.models import JSONField
from mptt.models import MPTTModel, TreeForeignKey
from account.models import Company, FuncStructure
from customer.models import Customer


# Список форм
class Form(models.Model):
    title = models.TextField(blank=True)
    size = models.CharField(max_length=10, null=True)
    orientation = models.CharField(max_length=10, null=True)
    old_id = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "forms"

    # Получить  список сталбцов
    def get_rows(self):
        return self.rows.select_related().order_by('position').all()


# Столбцы формы
class Row(models.Model):
    form = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name='rows')
    kind = models.CharField(max_length=15, null=True)
    position = models.IntegerField(null=True)
    classes = models.CharField(max_length=80, null=True, blank=True)
    group = models.IntegerField(null=True)

    class Meta:
        db_table = "rows"
        ordering = ['id']

    def __str__(self):
        return str(self.id)

    # Получить список маркеров
    def get_markers(self):
        return self.markers.order_by('id').all()


# Маркеры формы
class Marker(models.Model):
    KIND_CHOICES = (
        ('text', "Ввод текста"),
        ('textarea', "textarea"),
        ('select', "select"),
        ('parent', "parent"),
        ('datalist', 'datalist'),
        ('mkb10', 'mkb10'),
        ('customer', 'customer'),
        ('label', 'label'),
        ('datepicker', 'datepicker'),
        ('currentDate', 'currentDate'),
        ('checkbox', 'checkbox'),
        ('doctor', 'doctor'),
        ('currentTime', 'currentTime'),
        ('hidden', 'hidden'),
        ('mkb9', 'mkb9'),
        ('radio', 'radio'),
        ('nowdate', 'nowdate'),
        ('time', 'time'),
        ('drugs', 'drugs'),
        ('profile_bunk', 'profile_bunk'),
        ('scheme_chemotherapy', 'scheme_chemotherapy'),
        ('morphological_type', 'morphological_type'),
        ('postoperative_complication', 'postoperative_complication'),
        ('head', 'head'),
        ('departments', 'departments'),
        ('doctors', 'doctors'),
        ('doctors_bg', 'doctors_bg'),
        ('service', 'service'),
        ('multiple_parent', 'multiple_parent'),
        ('multiple_form_parent', 'multiple_form_parent'),
    )
    row = models.ForeignKey(Row, on_delete=models.CASCADE,
                            related_name='markers')
    name = models.CharField(max_length=80)
    label = models.TextField(max_length=240, null=True, blank=True)
    kind = models.CharField(
        max_length=80, choices=KIND_CHOICES, default='text')
    colspan = models.CharField(max_length=80, null=True)
    options = models.TextField(null=True, blank=True)
    is_bold = models.BooleanField(default=False)
    is_italic = models.BooleanField(default=False)
    is_center = models.BooleanField(default=False)
    is_border = models.BooleanField(default=False)
    is_rotated = models.BooleanField(default=False)
    is_required = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    grouping = models.CharField(max_length=80, null=True, blank=True)
    group_separator = models.CharField(max_length=80, null=True, blank=True)
    classes = models.CharField(max_length=80, null=True, blank=True)
    rowspan = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "markers"

    # Получить список маркеров
    def get_adaptivemarker(self):
        adaptivemarker = self.adaptivemarker_set
        if adaptivemarker.count():
            return adaptivemarker.last()
        return self


# Группировка форм
class GroupForm(models.Model):
    title = models.CharField(max_length=180, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "groupForms"


# Формы больницы
class CompanyForm(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    form = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name='hospital_forms')
    group = models.ForeignKey(GroupForm, on_delete=models.CASCADE,
                              null=True, blank=True,
                              related_name='group_forms')


# Формы отделении
class FuncStructureForm(models.Model):
    company_form = models.ForeignKey(
        CompanyForm, on_delete=models.CASCADE)
    func_structure = models.ForeignKey(
        FuncStructure, on_delete=models.CASCADE, null=True)


# Сохраненные формы
class FormHistory(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    form_data = JSONField(blank=True, null=True)
    referer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name='form_history_referers')
    status = models.IntegerField(null=True)
    temporary_form_data = JSONField(blank=True, null=True)
    hospital = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # Получить форму ИБ пациента
    def get_history(self):
        data = []
        grouped_list = []
        form_data = self.form_data
        form_id = self.form.id
        rows = Row.objects.filter(
            form__id=form_id).select_related().order_by(
            'position').all()
        for row in rows:
            item = {
                'id': row.id,
                'markers': [],
            }
            for marker in row.markers.all():
                if marker.grouping != '0':
                    if marker.grouping not in grouped_list:
                        marker_form_data = ''
                        group_result = Marker.objects.filter(
                            row__form__id=form_id,
                            grouping=marker.grouping).all()
                        for marker_group in group_result:
                            marker_group_data = form_data.get(
                                marker_group.name, '')
                            if marker_group_data:
                                label = marker_group.label + ' '
                                marker_form_data += label
                                if marker_group.kind == 'checkbox':
                                    for marker_val in marker_group_data:
                                        marker_form_data += marker_val + ';'
                                else:
                                    separator = marker_group.group_separator or ''
                                    marker_form_data += str(marker_group_data) + str(separator) + ' '
                        item['markers'].append(
                            {
                                'label': '',
                                'kind': 'grouped_marker',
                                'colspan': 12,
                                'form_data': marker_form_data
                            }
                        )
                        grouped_list.append(marker.grouping)
                else:
                    options = marker.options
                    marker_form_data = form_data.get(marker.name, '')
                    if options:
                        options = json.loads(marker.options)
                    item['markers'].append(
                        {
                            'name': marker.name,
                            'label': marker.label,
                            'kind': marker.kind,
                            'colspan': marker.colspan,
                            'is_bold': marker.is_bold,
                            'is_italic': marker.is_italic,
                            'is_center': marker.is_center,
                            'options': options,
                            'visible': marker.visible,
                            'classes': marker.classes,
                            'form_data': marker_form_data
                        }
                    )
            if len(item['markers']) > 0:
                data.append(item)
        return data

    # Сохранить историю
    def save_history(customer, data, form, history, status, user):
        history_id = None
        form_data = {}
        temporary_form_data = {}
        if history:
            form_data = history.form_data
            history_id = history.id
            form = history.form
        for row in form.get_rows():
            for marker in row.get_markers():
                name = marker.name
                if marker.kind == 'checkbox':
                    value = data.getlist(name)
                else:
                    value = data.get(name, '')
                if value:
                    if status == '1' or status == '2':
                        form_data.setdefault(name, value)
                    else:
                        temporary_form_data[name] = value

        obj, type_save = FormHistory.objects.update_or_create(
            pk=history_id,
            defaults={
                'form_data': form_data,
                'temporary_form_data': temporary_form_data,
                'user': user,
                'customer': customer,
                'form': form,
                'hospital': user.company,
                'status': status
            }
        )
        return obj.id


class AdaptiveMarker(models.Model):
    marker = models.ForeignKey(Marker, on_delete=models.CASCADE)
    kind = models.CharField(max_length=180, null=True)
    label = models.TextField(max_length=240, null=True)
    options = models.TextField(null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    func_structure = models.ForeignKey(FuncStructure,
                                       on_delete=models.CASCADE, null=True)
    visible = models.CharField(max_length=80, null=True)


# Готовые шаблоны
class ReadyPhrase(MPTTModel):
    marker = models.ForeignKey(Marker, on_delete=models.CASCADE)
    phrase = models.TextField(null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    def __str__(self):
        return self.phrase

    # Добавить готовые шаблоны
    def add(data):
        i = 0
        user = data.get('user')
        marker = data.get('marker')
        phrases = data.get('phrase', '')
        descriptions = data.get('phrase_description', '')
        while i < len(descriptions):
            description = descriptions[i]
            phrase = phrases[i]
            ReadyPhrase(marker_id=marker, phrase=phrase, user=user,
                        description=description).save()
            i += 1
        return ''

    def get_as_json(marker, parent=None, search=None):
        data = []
        tree_list = []
        ready_phrases = ReadyPhrase.objects.filter(marker=marker).all()
        if search:
            ready_phrases = ready_phrases.filter(phrase__icontains=search)
        else:
            ready_phrases = ready_phrases.filter(parent=parent)
        for ready_phrase in ready_phrases:
            tree_list.append(ready_phrase.id)
            if not ready_phrase.parent or ready_phrase.parent.id not in tree_list:
                item = {
                    'id': ready_phrase.id
                }
                name = ready_phrase.phrase
                if not ready_phrase.is_leaf_node():
                    item['load_on_demand'] = True
                else:
                    name = '<span class="get-phrase">' + name + '</span>'
                item['name'] = name
                data.append(item)
        return data
