import decimal
from django import template
from django.db.models import Sum

register = template.Library()


@register.simple_tag
def get_paid(val1, val2):
    invoice = val1 if val1 else val2
    return invoice


@register.simple_tag
def get_remainder(invoice, paid):
    return int(invoice) - int(paid)


@register.simple_tag
def set_condition_val(condition, val_true, val_false):
    if condition:
        return val_true
    return val_false
