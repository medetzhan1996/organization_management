from django import template
from django.db.models import Count
from analytics.models import ScheduleAnalytic

register = template.Library()


@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)


@register.simple_tag
def set_data_by_compare(val1, val2, data):
    if str(val1) == str(val2):
        return data
    else:
        return ''


@register.simple_tag
def get_quantity_schedule_by_status(query, status):
    result = query.filter(status=status).aggregate(
        quantity=Count('customer'))
    return result.get('quantity', 0)


@register.simple_tag
def get_quantity_primary_customer(customers, date):
    result = ScheduleAnalytic.get_quantity_primary_customers(customers, date)
    return result


@register.simple_tag
def get_repeated_schedule_customer(customers, date):
    result = ScheduleAnalytic.get_quantity_repeated_customers(customers, date)
    return result
