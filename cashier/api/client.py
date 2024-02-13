import requests
from requests.exceptions import ConnectionError
from django.conf import settings

api_url = settings.API_URL
api_token = settings.API_TOKEN


def api_invoice_create(service, performing_doctor, type_appeal, place, customer_insurance,
                       icd, customer, screen={}, screen_title=''):
    url_api = 'http://{}/api/invoice_management/invoice/create'.format(api_url)
    data = {
        'hospital': 'markezi_clinik',
        'service': service,
        'consumption': '0',
        'performing_doctor': performing_doctor,
        'type_appeal': type_appeal,
        'place': place,
        'customer_insurance': customer_insurance,
        'icd': icd,
        'customer': customer,
        'screen': screen,
        'screen_title': screen_title,

    }

    result = requests.post(url_api, data=data, headers={
        'Authorization': 'Token ' + api_token}, timeout=1)
    result.raise_for_status()
    return result.json()
