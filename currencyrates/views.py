import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Centralized API Request Handler
def fetch_taptapsend_data():
    """
    Makes a centralized request to the TapTapSend API and returns the parsed JSON response.
    """
    try:
        url = "https://api.taptapsend.com/api/fxRates"
        headers = {
            "appian-version": "web/2022-05-03.0",
            "x-device-id": "web",
            "x-device-model": "web"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from TapTapSend API: {e}")
        return None

# Endpoint: Fetch All Exchange Rates
@api_view(['GET'])
def all_exchange_rates(request):
    """
    Fetches all exchange rates directly from the TapTapSend API.
    """
    data = fetch_taptapsend_data()
    if data:
        return Response({'source': "Fetched from TapTapSend API", 'data': data})
    return Response({'error': "Failed to fetch data from TapTapSend API"}, status=500)

# Endpoint: Fetch CAD Exchange Rates
@api_view(['GET'])
def fetch_cad_exchange_rates(request):
    """
    Fetches exchange rates for CAD, categorizing local and non-local (e.g., USD) currencies.
    """
    data = fetch_taptapsend_data()
    if data:
        cad_data = next((country for country in data['availableCountries'] if country['currency'] == 'CAD'), None)
        if cad_data:
            processed_data = [
                {
                    'isoCountryCode': corridor.get('isoCountryCode', ''),
                    'countryDisplayName': corridor.get('countryDisplayName', ''),
                    'currency': corridor.get('currency', ''),
                    'fxRate': corridor.get('fxRate', ''),
                    'isLocalCurrency': corridor.get('currency') != 'USD'  # Mark as local if not USD
                }
                for corridor in cad_data.get('corridors', [])
            ]
            return Response({'source': "Fetched from TapTapSend API", 'data': processed_data})
        return Response({'error': "CAD data not found"}, status=404)
    return Response({'error': "Failed to fetch data from TapTapSend API"}, status=500)

# Endpoint: Fetch CAD Available Currencies
@api_view(['GET'])
def fetch_cad_available_currencies(request):
    """
    Fetches a list of all currencies available for CAD equivalency, 
    along with their country names and whether the currency is local or a fallback like USD.
    """
    data = fetch_taptapsend_data()
    if data:
        cad_data = next((country for country in data['availableCountries'] if country['currency'] == 'CAD'), None)
        if cad_data:
            currencies = [
                {
                    'Country Code': corridor.get('isoCountryCode', ''),
                    'Country Display Name': corridor.get('countryDisplayName', ''),
                    'Currency': corridor['currency'],
                    'Is Local Currency': corridor.get('currency') != 'USD'  # Mark as local if not USD
                }
                for corridor in cad_data.get('corridors', [])
            ]
            return Response({'source': "Fetched from TapTapSend API", 'currencies': currencies})
        return Response({'error': "CAD data not found"}, status=404)
    return Response({'error': "Failed to fetch data from TapTapSend API"}, status=500)

@api_view(['GET'])
def cad_conversion(request):
    """
    Fetches exchange rate for CAD to a specific currency (with additional validation for USD).
    Requires `currency` and `CountryCode` parameters when the currency is USD.
    """
    try:
        # Fetch the required parameters
        currency_code = request.query_params.get('currency', None) 
        iso_country_code = request.query_params.get('CountryCode', None)  

        # Validate that the currency parameter is provided
        if not currency_code:
            return Response({'error': "Currency parameter is required ?currency=PHP)"}, status=400)

        # Fetch data from the TapTapSend API
        data = fetch_taptapsend_data()
        if data:
            # Filter for CAD exchange rates
            cad_data = next((country for country in data['availableCountries'] if country['currency'] == 'CAD'), None)
            if cad_data:
                # If currency is USD and not local, validate isoCountryCode
                if currency_code == 'USD':
                    if not iso_country_code:
                        return Response({
                            'error': "Country Code parameter (isoCountryCode) is required for USD (e.g., ?isoCountryCode=LB)"
                        }, status=400)
                    # Filter for USD based on both currency and Country Code
                    currency_data = next(
                        (corridor for corridor in cad_data['corridors']
                         if corridor['currency'] == currency_code and corridor.get('isoCountryCode') == iso_country_code),
                        None
                    )
                else:
                    # Filter for other currencies
                    currency_data = next(
                        (corridor for corridor in cad_data['corridors'] if corridor['currency'] == currency_code),
                        None
                    )

                # Return the result if found
                if currency_data:
                    return Response({'source': "Fetched from TapTapSend API", 'data': currency_data})
                else:
                    available_currencies = [
                        {
                            'currency': corridor['currency'],
                            'CountryCode': corridor.get('isoCountryCode', '')
                        }
                        for corridor in cad_data['corridors']
                    ]
                    return Response({
                        'error': f"Data for currency '{currency_code}' with Country Code '{iso_country_code}' not found.",
                        'available_currencies': available_currencies
                    }, status=404)
            else:
                return Response({'error': "CAD data not found in the API response"}, status=404)

        return Response({'error': "Failed to fetch data from TapTapSend API"}, status=500)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return Response({'error': "Failed to fetch data from TapTapSend API"}, status=500)
