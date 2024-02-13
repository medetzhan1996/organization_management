from modal_convert.convert import ConvertToListOfDict
from .models import Schedule, ScheduleEquipment


class ScheduleConvert(ConvertToListOfDict):

    class Meta:
        model = Schedule
        fields = {
            'start_time': 'start_datetime',
            'end_time': 'end_datetime'
        }


class ScheduleUserConvert(ConvertToListOfDict):

    class Meta:
        model = Schedule
        fields = {
            'id': 'pk',
            'title': 'customer__name',
            'start': 'start_datetime',
            'end': 'end_datetime',
            'resourceId': 'object_id',
            'status': 'status'
        }
        extra = {
            'extendedProps': {
                'icon': 'test..'
            }
        }


class ScheduleEquipmentConvert(ConvertToListOfDict):

    class Meta:
        model = ScheduleEquipment
        fields = {
            'id': 'schedule__pk',
            'title': 'schedule__customer__name',
            'start': 'schedule__start_datetime',
            'end': 'schedule__end_datetime',
            'resourceId': 'equipment__pk'
        }
