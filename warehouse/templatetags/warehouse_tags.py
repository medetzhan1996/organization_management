from django import template
register = template.Library()


# Получить остаток товара
@register.simple_tag
def get_remainder(storage_good_operation):
    arrival = storage_good_operation.get_remainder(1) or 0
    movement = storage_good_operation.get_remainder(2) or 0
    write_off = storage_good_operation.get_remainder(3) or 0
    sale = storage_good_operation.get_remainder(4) or 0
    return arrival - write_off - sale - movement
