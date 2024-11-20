import requests
from requests.exceptions import ConnectionError
from django.conf import settings

def get_customer_by_iin(iin):
    api_url = settings.INSURANCE_API_URL
    api_token = settings.INSURANCE_API_TOKEN
    url_customer_search_api = 'http://{}/api/customer_management/customer/{}/detail'.format(api_url, iin)
    try:
        result = requests.get(url_customer_search_api, headers={
            'Authorization': 'Token ' + api_token}, timeout=30)
        result.raise_for_status()
        return result.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.ConnectionError as err:
        print(f"Error connecting to the server: {err}")
    except requests.exceptions.Timeout:
        print("Timeout occurred")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

def get_customer_professional_examination_by_iin(iin):
    CUSTOMER_CABINET_API_URL = settings.CUSTOMER_CABINET_API_URL
    CUSTOMER_CABINET_API_TOKEN = settings.CUSTOMER_CABINET_API_TOKEN
    CUSTOMER_CABINET_INSURANCE = settings.CUSTOMER_CABINET_INSURANCE
    url_customer_search_api = 'http://{}/api/customer_personal_cabinet/customer/professional/examination?insurance={}&iin={}'.format(CUSTOMER_CABINET_API_URL, CUSTOMER_CABINET_INSURANCE, iin)
    try:
        result = requests.get(url_customer_search_api, headers={
            'Authorization': 'Token ' + CUSTOMER_CABINET_API_TOKEN})
        result.raise_for_status()
        print(result.json())
        return result.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.ConnectionError as err:
        print(f"Error connecting to the server: {err}")
    except requests.exceptions.Timeout:
        print("Timeout occurred")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")