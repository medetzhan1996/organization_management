from datetime import datetime, timedelta
from django import template

register = template.Library()


@register.simple_tag
def get_calendar_display_users(query):
    return query.filter(is_display_calendar=True).all()


@register.simple_tag
def get_val(val):
    return val


@register.simple_tag
def selected_by_content_type(instance, object_id, content_type):
    if instance and object_id == instance.object_id and content_type == instance.content_type.id:
        return 'selected'
    else:
        return ''


@register.simple_tag
def condition_set_class(condition, class1, class2):
    if condition:
        return class1
    else:
        return class2


@register.simple_tag
def compare_set(condition1, condition2, class1, class2=''):
    if condition1 == condition2:
        return class1
    else:
        return class2


@register.simple_tag
def is_selected(val1, val2):
    if str(val1) == str(val2):
        return 'selected'
    else:
        return ''


@register.simple_tag
def time_format(time):
    return time.strftime("%H:%M")


@register.simple_tag
def get_week_time(query, week):
    if query:
        return query.filter(week=week).all()
    return []


@register.simple_tag
def get_time_interval(start, end, interval=15):
    times = []
    delta = timedelta(minutes=interval)
    start = datetime.strptime(start, '%H:%M:%S')
    end = datetime.strptime(end, '%H:%M:%S')
    time = start
    while time <= end:
        times.append(time)
        time += delta
    return times


@register.simple_tag
def get_times():
    times = {
        '5': '5 мин',
        '10': '10 мин',
        '15': '15 мин',
        '20': '20 мин',
        '25': '25 мин',
        '30': '30 мин',
        '35': '35 мин',
        '40': '40 мин',
        '45': '45 мин',
        '50': '50 мин',
        '55': '55 мин',
        '60': '1 ч',
        '65': '1 ч 5 мин',
        '70': '1 ч 10 мин',
        '75': '1 ч 15 мин',
        '80': '1 ч 20 мин',
        '85': '1 ч 25 мин',
        '90': '1 ч 30 мин',
        '95': '1 ч 35 мин',
        '100': '1 ч 40 мин',
        '105': '1 ч 45 мин',
        '110': '1 ч 50 мин',
        '115': '1 ч 55 мин',
        '120': '2 ч',
    }
    return times


@register.simple_tag
def set_attr_duration(duration):
    return "duration:{}".format(duration)


@register.simple_tag
def set_active_class(view_name, *args):
    if view_name in args:
        return 'active'
    return ''
