from datetime import datetime, timedelta


class RegisterUtils:

    @staticmethod
    def is_between(appoints, start_time, end_time):
        for appoint in appoints:
            appoint_start_time = appoint.get('start_time')
            appoint_end_time = appoint.get('end_time')
            if appoint_start_time <= start_time < appoint_end_time \
                    or appoint_start_time <= end_time < appoint_end_time:
                return True
        return False

    @staticmethod
    def get_slots_with_compress(
            hours, appointments, duration=timedelta(minutes=20)):
        duration = timedelta(minutes=20)
        start_times = []
        slots = sorted([(hours[0], hours[0])] +
                       appointments + [(hours[1], hours[1])])
        start_house = hours[0]
        end_house = hours[1]
        for i in range(len(slots) - 1):
            start = slots[i][1]
            end = slots[i + 1][0]
            if start >= start_house and end <= end_house:
                while start + duration <= end:
                    start_time = "{:%H:%M}".format(start)
                    start += duration
        return True

    @staticmethod
    def get_free_slots(appoints, start_work, end_work, slot=15):
        times = []
        slot = timedelta(minutes=slot)
        start_work = datetime.strptime(start_work, '%H:%M:%S')
        end_work = datetime.strptime(end_work, '%H:%M:%S')
        while start_work <= end_work:
            start_time = start_work.time()
            end_time = (start_work + slot).time()
            if not RegisterUtils.is_between(
                    appoints, start_time, end_time):
                times.append(start_time)
            start_work += slot
        return times

    @staticmethod
    def get_end_datetime(start_date_time, duration):
        end_datetime = start_date_time + timedelta(minutes=duration)
        return end_datetime

    @staticmethod
    def get_datetime(date, time):
        date = datetime. strptime(date, '%Y-%m-%d').date()
        time = datetime. strptime(time, '%H:%M:%S').time()
        return datetime.combine(date, time)

    @staticmethod
    def get_duration(start_datetime, end_datetime):
        minutes_diff = (end_datetime - start_datetime
                        ).total_seconds() / 60.0
        return int(minutes_diff)
