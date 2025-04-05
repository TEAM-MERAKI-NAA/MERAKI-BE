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
    Fetches exchange rate for CAD to a specific currency.
    For USD currency, ensures that `CountryCode` is provided.
    Includes alerts for validating the currency code and proper usage for USD.
    """
    try:
        # Fetch the required parameters
        currency_code = request.query_params.get('currency', None)  # E.g., 'USD', 'PHP', etc.
        country_code = request.query_params.get('CountryCode', None)  # E.g., 'EG', 'LB', etc.

        # Validate that the currency parameter is provided
        if not currency_code:
            return Response({
                'error': "Missing parameter: 'currency' is required to fetch exchange rates.",
                'details': "Ensure you include the 'currency' parameter in your query (e.g., ?currency=USD).",
                'help': "Refer to 'currencyrates/exchange-rates/cad/currencies/' for valid currencies and country codes."
            }, status=400)

        # Fetch data from the TapTapSend API
        data = fetch_taptapsend_data()
        if data:
            # Filter for CAD exchange rates
            cad_data = next((country for country in data['availableCountries'] if country['currency'] == 'CAD'), None)
            if cad_data:
                # Validate the provided currency code
                valid_currencies = [
                    corridor['currency'] for corridor in cad_data['corridors']
                ]
                if currency_code not in valid_currencies:
                    return Response({
                        'error': f"Invalid currency: '{currency_code}' is not supported.",
                        'details': "The currency you provided is not listed as valid for CAD exchange rates.",
                        'help': "Refer to 'IPaddress:8000/currencyrates/exchange-rates/cad/currencies/' for a list of valid currencies and country codes."
                    }, status=404)

                if currency_code == 'USD':
                    # Validate CountryCode for USD currency
                    if not country_code:
                        return Response({
                            'error': "Missing parameter: 'CountryCode' is required for USD currency.",
                            'details': "Provide the 'CountryCode' parameter in your query (e.g., ?currency=USD&CountryCode=EG).",
                            'help': "Refer to 'IPaddress:8000/currencyrates/exchange-rates/cad/currencies/' for countries that support USD."
                        }, status=400)

                    # Filter for USD equivalency based on Country Code
                    currency_data = next(
                        (corridor for corridor in cad_data['corridors']
                         if corridor['currency'] == currency_code and corridor.get('isoCountryCode') == country_code),
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
                    return Response({
                        'error': f"Invalid combination: No data found for 'currency={currency_code}' with 'CountryCode={country_code}'.",
                        'details': f"The provided currency '{currency_code}' and country code '{country_code}' do not match available data.",
                        'help': "Refer to 'currencyrates/exchange-rates/cad/currencies/' for valid combinations of currencies and country codes."
                    }, status=404)
            else:
                return Response({
                    'error': "Data unavailable: CAD-specific data could not be retrieved from the API.",
                    'details': "Please verify if CAD data is available or contact support for assistance."
                }, status=404)

        return Response({
            'error': "Service error: Failed to fetch data from the TapTapSend API.",
            'details': "This may be due to connectivity issues or a problem with the external API."
        }, status=500)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return Response({
            'error': "Unexpected error occurred while processing your request.",
            'details': "Please try again later or contact support if the issue persists."
        }, status=500)
