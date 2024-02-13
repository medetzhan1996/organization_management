import requests
from requests.exceptions import ConnectionError
from django.conf import settings

api_url = settings.API_URL
api_token = settings.API_TOKEN

def get_customer_by_iin(iin):
    url_customer_search_api = 'http://{}/api/customer_management/customer/{}/detail'.format(api_url, iin)
    try:
        result = requests.get(url_customer_search_api, headers={
            'Authorization': 'Token ' + api_token}, timeout=1)
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

api2_url = '82.200.165.222:19603'
api2_token = '020a2cef2f0e05ece1e8ccb85f35706a28c75735'
insurance = 'insurance1'

def get_customer_professional_examination_by_iin(iin):
    url_customer_search_api = 'http://{}/api/customer_personal_cabinet/customer/professional/examination?insurance={}&iin={}'.format(api2_url, insurance, iin)
    try:
        result = requests.get(url_customer_search_api, headers={
            'Authorization': 'Token ' + api2_token})
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