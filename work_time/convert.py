from datetime import datetime, timedelta
from modal_convert.convert import ConvertToListOfDict
from .models import WorkTimeExclusion, WorkTime


class WorkTimeExclusionConvert(ConvertToListOfDict):

    class Meta:
        model = WorkTimeExclusion
        fields = {
            'resourceId': 'object_id',
            'start': 'start_datetime',
            'end': 'end_datetime',
        }
        extra = {
            'groupId': '1',
            'display': 'inverse-background',
            'className': 'fc-bgevent',
        }


class WorkTimeConvert(ConvertToListOfDict):

    class Meta:
        model = WorkTime
        fields = {
            'resourceId': 'object_id'
        }
        extra = {
            'groupId': '1',
            'display': 'inverse-background',
            'className': 'fc-bgevent',
        }

    def week_to_date(self, start_date, end_date):
        data = []
        delta = timedelta(days=1)
        while start_date <= end_date:
            week = start_date.weekday()
            queryset = self.queryset.filter(week=week).all()
            for query in queryset:
                item = self.convert_to_dict(query)
                item['start'] = datetime.combine(start_date, query.start_time)
                item['end'] = datetime.combine(start_date, query.end_time)
                data.append(item)
            start_date += delta
        return data
