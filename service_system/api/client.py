import requests
from requests.exceptions import ConnectionError
from django.conf import settings

api_url = settings.API_URL
api_token = settings.API_TOKEN


def get_covered_services(card_number, hospital, icd, type_appeal, place):
    url_api = 'http://{}/api/invoice_management/performed/services'.format(api_url)
    data = {
        'card_number': card_number,
        'hospital': hospital,
        'icd': icd,
        'type_appeal': type_appeal,
        'place': place
    }
    result = requests.post(url_api, data=data, headers={
        'Authorization': 'Token ' + api_token}, timeout=1)
    result.raise_for_status()
    return result.json()
