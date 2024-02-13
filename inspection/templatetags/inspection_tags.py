from datetime import datetime
from django import template
from django.db.models import Count
from register.models import Schedule

register = template.Library()


@register.simple_tag
def week_name_date(date):
    days = ["Пн", "Вт", "Ср", "Чт", "Пн", "Сб", "Вс"]
    dayNumber = date.weekday()
    return days[dayNumber]


@register.simple_tag
def get_schedule_group_by_date(schedules, date):
    return Schedule.get_group_by_date(schedules, date)


@register.simple_tag
def get_schedule_group_by_customer(schedules, date):
    return Schedule.get_group_by_customer(schedules, date)


@register.simple_tag
def get_schedule_by_date(schedules, date):
    return schedules.filter(
              start_datetime__date=date
    ).order_by('start_datetime')


@register.simple_tag
def get_week_by_date(date):
    return datetime.strptime(date, "%Y-%m-%d").strftime('%Y-W%V')


@register.simple_tag
def get_duration_time(datetime_start, datetime_end):
    minutes_diff = (datetime_end - datetime_start).total_seconds() / 60.0
    return int(minutes_diff)


@register.simple_tag
def is_selected(val1, val2):
    if val1 == val2:
        return 'selected'
    else:
        return ''


@register.simple_tag
def group_by_date(qs):
    qs = qs.values('start_datetime__date').annotate(
        available=Count('id'))
    return qs


@register.simple_tag
def compare_set_class(val1, val2, class1, class2=''):
    if val1 == val2:
        return class1
    return class2
