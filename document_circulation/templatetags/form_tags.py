import json
from django.urls import reverse
from django import template
from django.utils.safestring import mark_safe
import markdown
from document_circulation.models import FormHistory
register = template.Library()


@register.simple_tag
def get_adaptivemarker(marker):
    return marker.get_adaptivemarker()


@register.simple_tag
def compare_set(condition1, condition2, class1, class2=''):
    if condition1 == condition2:
        return class1
    else:
        return class2


@register.simple_tag
def get_history_data(marker, history):
    if history:
        form_data = history.form_data.get(marker.name, '')
        temporary_form_data = history.temporary_form_data.get(marker.name, '')
        if form_data:
            return {'is_contenteditable': '', 'data': form_data}
        elif temporary_form_data:
            return {'is_contenteditable': 'contenteditable=true',
                    'data': temporary_form_data}
    return {'is_contenteditable': 'contenteditable=true', 'data': ''}


@register.simple_tag
def get_relation_form_data(customer, adaptivemarker, history=None):
    relation_form_data = {}
    relation_data = ''
    if adaptivemarker.kind == 'parent':
        options = json.loads(adaptivemarker.options)
        relation_form_id = options['form_id']
        relation_markers = options['markers']
        if relation_form_id not in relation_form_data:
            for relation_marker in relation_markers:
                relation_history = FormHistory.objects.filter(
                    customer=customer,
                    form=relation_form_id
                )
                if history:
                    relation_history = relation_history.exclude(id=history.id)
                if relation_history.exists():
                    form_data = relation_history.last().form_data
                    relation_form_data[relation_form_id] = form_data
        data = relation_form_data.get(relation_form_id, '')
        if data:
            result = data.get(relation_marker, '')
            if result:
                relation_data += result + ';'
    return relation_data


@register.simple_tag
def get_data(data):
    if data:
        return data
    return ''


@register.simple_tag
def get_key(key):
    if key and key == '0':
        return ''
    else:
        return key


@register.simple_tag
def is_center(is_center):
    if is_center == '1':
        return 'text-center'


@register.simple_tag
def text_bold(is_bold):
    if is_bold:
        return 'fw-bold'
    return ''

@register.simple_tag
def text_center(is_bold):
    if is_bold:
        return 'text-center'
    return ''


@register.simple_tag
def get_selected_option(key, val):
    if key == val:
        return 'selected'
    else:
        return ''


@register.simple_tag
def is_selected_history(history, history_selected):
    if history and history.id == history_selected:
        return 'active'
    else:
        return ''


@register.simple_tag
def is_checked(val, dataList):
    if val and dataList:
        if val in dataList:
            return 'checked'
    else:
        return None


@register.simple_tag
def is_disabled(formData):
    if formData:
        return 'disabled'


@register.simple_tag
def ready_marker(marker_id):
    if marker_id:
        classes = 'pull-right ready-phrase'
        output = '<span data-id="' + \
            str(marker_id) + '" class="' + classes + '">&#10010;</span>'
        return output


@register.simple_tag
def json_load(data):
    return json.loads(data)


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def get_status(status, date_time):
    if status == 1:
        return {'title': 'pdf', 'class': 'over'}
    elif status == 2:
        return {'title': 'временная форма', 'class': 'over'}
    elif status == 3:
        return {'title': 'незавершенная форма', 'class': 'over'}
    elif status == 4:
        return {'title': 'направленная форма', 'class': 'directed'}


@register.simple_tag
def get_form_url(customer, history):
    return reverse('document_circulation:form_in_history', kwargs={
        'history': history.id, 'customer': customer.id})


@register.simple_tag
def is_pdf(history):
    if history and history.status == 1:
        return True
    return False


@register.simple_tag
def relation_create(marker_id, kind):
    classes = 'pull-right form-relation-modal'
    content = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Capa_1" x="0px" y="0px" width="13px" height="13px" viewBox="0 0 528.899 528.899" fill="#c5c5c5" xml:space="preserve"><g><path d="M328.883,89.125l107.59,107.589l-272.34,272.34L56.604,361.465L328.883,89.125z M518.113,63.177l-47.981-47.981   c-18.543-18.543-48.653-18.543-67.259,0l-45.961,45.961l107.59,107.59l53.611-53.611   C532.495,100.753,532.495,77.559,518.113,63.177z M0.3,512.69c-1.958,8.812,5.998,16.708,14.811,14.565l119.891-29.069   L27.473,390.597L0.3,512.69z"/></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>'
    output = '<span data-id="' + \
        str(marker_id) + '" class="' + classes + \
        '">' + content + '</span>'
    return output


@register.simple_tag
def get_ready_phrase(marker_id):
    classes = 'pull-right get-phrase-modal'
    content = '&#x2b;'
    output = '<span data-marker="' + \
        str(marker_id) + '" class="' + classes + \
        '">' + content + '</span>'
    return output


@register.simple_tag
def audio_input(marker_id):
    classes = 'pull-right get-audio-modal'
    content = '<svg xmlns="http://www.w3.org/2000/svg" fill="#95b0d2" viewBox="0 0 50 50" width="15px" height="15px"><path d="M 18 3 C 16.346 3 15 4.346 15 6 L 15 24 L 35 24 L 35 6 C 35 4.346 33.654 3 32 3 L 18 3 z M 11.984375 17.986328 A 1.0001 1.0001 0 0 0 11 19 L 11 34 C 11 37.301625 13.698375 40 17 40 L 22 40 L 22 46 L 17 46 A 1.0001 1.0001 0 1 0 17 48 L 33 48 A 1.0001 1.0001 0 1 0 33 46 L 28 46 L 28 40 L 33 40 C 36.301625 40 39 37.301625 39 34 L 39 19 A 1.0001 1.0001 0 1 0 37 19 L 37 34 C 37 36.220375 35.220375 38 33 38 L 17 38 C 14.779625 38 13 36.220375 13 34 L 13 19 A 1.0001 1.0001 0 0 0 11.984375 17.986328 z M 15 26 L 15 33 C 15 34.654 16.346 36 18 36 L 32 36 C 33.654 36 35 34.654 35 33 L 35 26 L 15 26 z M 25 29 C 26.105 29 27 29.895 27 31 C 27 32.105 26.105 33 25 33 C 23.895 33 23 32.105 23 31 C 23 29.895 23.895 29 25 29 z"/></svg>'
    output = '<span data-marker="' + \
        str(marker_id) + '" class="' + classes + \
        '">' + content + '</span>'
    return output


@register.simple_tag
def set_value_by_compare(val1, val2, result_true, result_false=''):
    if val1 == val2:
        return result_true
    return result_false


@register.simple_tag
def set_value_by_condition(condition, result_true, result_false=''):
    if condition:
        return result_true
    return result_false


@register.simple_tag
def display_symbol(symbol, count=1):
    return symbol * count
