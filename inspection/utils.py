from datetime import datetime, timedelta


class InspectionUtils:

    @staticmethod
    def get_start_end_week(date):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        start = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end = start + timedelta(days=6)
        return {'start_date': start, 'end_date': end}
