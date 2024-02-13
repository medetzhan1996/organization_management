# services.py
import requests
from requests.exceptions import JSONDecodeError


from datetime import timedelta, datetime
from django.contrib.contenttypes.models import ContentType
from register.models import Schedule
from account.models import User

def get_free_slots(doctor, date):
    working_hours_start = datetime.combine(date, datetime.min.time()) + timedelta(hours=9)  # 09:00
    working_hours_end = datetime.combine(date, datetime.min.time()) + timedelta(hours=18)  # 18:00
    lunch_break_start = datetime.combine(date, datetime.min.time()) + timedelta(hours=13)  # 13:00
    lunch_break_end = lunch_break_start + timedelta(hours=1)  # 14:00

    doctor_content_type = ContentType.objects.get_for_model(doctor)

    occupied_slots = Schedule.objects.filter(
        content_type=doctor_content_type, object_id=doctor.id, start_datetime__date=date
    ).values_list('start_datetime', flat=True)

    free_slots = []
    current_time = working_hours_start

    while current_time < working_hours_end:
        # Проверка на перерыв на обед
        if lunch_break_start <= current_time < lunch_break_end:
            current_time = lunch_break_end
            continue

        # Если время + длительность слота меньше времени окончания рабочего дня и слот свободен
        if current_time + timedelta(minutes=30) <= working_hours_end and current_time not in occupied_slots:
            free_slots.append(current_time.time().strftime('%H:%M'))

        current_time += timedelta(minutes=30)  # Инкрементируем на длительность слота (по умолчанию 30 минут)

    return free_slots
    pass

def get_free_slots_for_specializations_in_date_range(specializations, start_date, end_date):
    if not specializations:
        doctors = User.objects.all()
    else:
        doctors = User.objects.filter(speciality__title__in=specializations)

    result = {}
    current_date = start_date

    while current_date <= end_date:
        for doctor in doctors:
            slots = get_free_slots(doctor, current_date)
            if slots:
                # speciality = doctor.speciality.id
                speciality = doctor.speciality.title
                if speciality not in result:
                    result[speciality] = {}
                if doctor.id not in result[speciality]:
                    # result[speciality][doctor.id] = {}
                    result[speciality][doctor.doctor_code] = {}
                result[speciality][doctor.doctor_code][str(current_date)] = slots

        current_date += timedelta(days=1)

    return result


def create_examination_result(data):
    print(data, '===========')
    result = []
    url_api = '82.200.165.222:19603'
    token_api = '880430a839696607383313b109e5a0599617219b'
    print(type(data.get('examination_appointment')), '======================')
    json_data = {
        'examination_appointment': data.get('examination_appointment'),
        'icd': data.get('icd'),
        'conclusion': data.get('conclusion'),
        'recommendations': data.get('recommendations'),
    }
    url_invoice_api = 'http://82.200.165.222:19603/api/customer_personal_cabinet/api/examination/result'
    result = requests.post(url_invoice_api, data=json_data, headers={'Authorization': 'Token ' + token_api})
    return result.json()
