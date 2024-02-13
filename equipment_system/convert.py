from modal_convert.convert import ConvertToListOfDict
from .models import Equipment


class EquipmentConvert(ConvertToListOfDict):

    class Meta:
        model = Equipment
        fields = {
            'id': 'pk',
            'title': 'title'
        }
        extra = {
            'extendedProps': {
                'resource': 'equipment'
            }
        }
