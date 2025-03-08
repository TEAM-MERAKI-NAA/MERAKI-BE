import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def fetch_exchange_rates(request):
    try:
        # Define the API URL and headers
        url = "https://api.taptapsend.com/api/fxRates"
        headers = {
            "appian-version": "web/2022-05-03.0",
            "x-device-id": "web",
            "x-device-model": ""
        }

        # Make the API request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Return the response data
        return Response({'source': "Fetched from TapTapSend API", 'data': data})

    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return Response({'error': "Failed to fetch data from TapTapSend API"}, status=500)
  
@api_view(['GET'])
def fetch_cad_exchange_rates(request):
    try:
        url = "https://api.taptapsend.com/api/fxRates"
        headers = {
            "appian-version": "web/2022-05-03.0",
            "x-device-id": "",
            "x-device-model": ""
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Filter for CAD exchange rates
        cad_data = next((country for country in data['availableCountries'] if country['currency'] == 'CAD'), None)
        if cad_data:
            return Response({'source': "Fetched from TapTapSend API", 'data': cad_data})
        else:
            return Response({'error': "CAD data not found"}, status=404)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching CAD exchange rates: {e}")
        return Response({'error': "Failed to fetch CAD data from TapTapSend API"}, status=500)

def fetch_cad_to_currency(request, currency_code):
    try:
        url = "https://api.taptapsend.com/api/fxRates"
        headers = {
            "appian-version": "web/2022-05-03.0",
            "x-device-id": "web",
            "x-device-model": ""
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Filter for CAD exchange rates
        cad_data = next((country for country in data['availableCountries'] if country['currency'] == 'CAD'), None)
        if cad_data:
            currency_data = next((corridor for corridor in cad_data['corridors'] if corridor['currency'] == currency_code), None)
            if currency_data:
                return Response({'source': "Fetched from TapTapSend API", 'data': currency_data})
            else:
                return Response({'error': f"{currency_code} data not found"}, status=404)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching CAD to {currency_code} exchange rate: {e}")
        return Response({'error': f"Failed to fetch CAD to {currency_code} data from TapTapSend API"}, status=500)

@api_view(['GET'])
def cad_to_php(request):
    return fetch_cad_to_currency(request, 'PHP')

@api_view(['GET'])
def cad_to_bdt(request):
    return fetch_cad_to_currency(request, 'BDT')

@api_view(['GET'])
def cad_to_brl(request):
    return fetch_cad_to_currency(request, 'BRL')

@api_view(['GET'])
def cad_to_usd(request):
    return fetch_cad_to_currency(request, 'USD')

@api_view(['GET'])
def cad_to_xaf(request):
    return fetch_cad_to_currency(request, 'XAF')

@api_view(['GET'])
def cad_to_cop(request):
    return fetch_cad_to_currency(request, 'COP')

@api_view(['GET'])
def cad_to_dop(request):
    return fetch_cad_to_currency(request, 'DOP')

@api_view(['GET'])
def cad_to_egp(request):
    return fetch_cad_to_currency(request, 'EGP')

@api_view(['GET'])
def cad_to_etb(request):
    return fetch_cad_to_currency(request, 'ETB')

@api_view(['GET'])
def cad_to_gtq(request):
    return fetch_cad_to_currency(request, 'GTQ')

@api_view(['GET'])
def cad_to_gnf(request):
    return fetch_cad_to_currency(request, 'GNF')

@api_view(['GET'])
def cad_to_htg(request):
    return fetch_cad_to_currency(request, 'HTG')

@api_view(['GET'])
def cad_to_inr(request):
    return fetch_cad_to_currency(request, 'INR')

@api_view(['GET'])
def cad_to_xof(request):
    return fetch_cad_to_currency(request, 'XOF')

@api_view(['GET'])
def cad_to_jmd(request):
    return fetch_cad_to_currency(request, 'JMD')

@api_view(['GET'])
def cad_to_kes(request):
    return fetch_cad_to_currency(request, 'KES')

@api_view(['GET'])
def cad_to_mga(request):
    return fetch_cad_to_currency(request, 'MGA')

@api_view(['GET'])
def cad_to_mxn(request):
    return fetch_cad_to_currency(request, 'MXN')

@api_view(['GET'])
def cad_to_mad(request):
    return fetch_cad_to_currency(request, 'MAD')

@api_view(['GET'])
def cad_to_npr(request):
    return fetch_cad_to_currency(request, 'NPR')

@api_view(['GET'])
def cad_to_ngn(request):
    return fetch_cad_to_currency(request, 'NGN')

@api_view(['GET'])
def cad_to_pkr(request):
    return fetch_cad_to_currency(request, 'PKR')

@api_view(['GET'])
def cad_to_lkr(request):
    return fetch_cad_to_currency(request, 'LKR')

@api_view(['GET'])
def cad_to_tzs(request):
    return fetch_cad_to_currency(request, 'TZS')

@api_view(['GET'])
def cad_to_gmd(request):
    return fetch_cad_to_currency(request, 'GMD')

@api_view(['GET'])
def cad_to_tnd(request):
    return fetch_cad_to_currency(request, 'TND')

@api_view(['GET'])
def cad_to_try(request):
    return fetch_cad_to_currency(request, 'TRY')

@api_view(['GET'])
def cad_to_ugx(request):
    return fetch_cad_to_currency(request, 'UGX')

@api_view(['GET'])
def cad_to_vnd(request):
    return fetch_cad_to_currency(request, 'VND')

@api_view(['GET'])
def cad_to_zmw(request):
    return fetch_cad_to_currency(request, 'ZMW')