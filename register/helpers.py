from datetime import datetime, timedelta


def is_between(appoints, start_time, end_time):
    for appoint in appoints:
        appoint_start_time = appoint.get('start').time()
        appoint_end_time = appoint.get('end').time()
        if appoint_start_time <= start_time < appoint_end_time \
                or appoint_start_time < end_time < appoint_end_time:
            return True
    return False


def get_free_slots(appoints, start_work, end_work, slot=15):
    times = []
    slot = timedelta(minutes=slot)
    start_work = datetime.strptime(start_work, '%H:%M:%S')
    end_work = datetime.strptime(end_work, '%H:%M:%S')
    while start_work <= end_work:
        start_time = start_work.time()
        end_time = (start_work + slot).time()
        if not is_between(appoints, start_time, end_time):
            times.append(start_time)
        start_work += slot
    return times
