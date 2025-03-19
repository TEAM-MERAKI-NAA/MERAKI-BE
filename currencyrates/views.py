import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def all_exchange_rates(request):
    try:
        # Define the API URL and headers
        url = "https://api.taptapsend.com/api/fxRates"
        headers = {
            "appian-version": "web/2022-05-03.0",
            "x-device-id": "web",
            "x-device-model": "web"
        }

        # Make the API request
        response = requests.get(url, headers=headers)
        response.raise_for_status() 

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
            "x-device-id": "web",
            "x-device-model": "web"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  
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


@api_view(['GET'])
def fetch_cad_available_currencies(request):
    """
    Fetches a list of all currencies available for CAD equivalency along with their country names and their respective currency.
    """
    try:
        # Define the API URL and headers
        url = "https://api.taptapsend.com/api/fxRates"
        headers = {
            "appian-version": "web/2022-05-03.0",
            "x-device-id": "web",
            "x-device-model": "web"
        }

        # Make the API request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Filter for CAD exchange rates
        cad_data = next((country for country in data['availableCountries'] if country['currency'] == 'CAD'), None)

        # If CAD data is found, extract the corridors data
        if cad_data:
            currencies = [
                {
                    'Country Code': corridor.get('isoCountryCode', ''),
                    'Country Display Name': corridor.get('countryDisplayName', ''),
                    'Currency': corridor['currency']
                }
                for corridor in cad_data.get('corridors', [])
            ]
            return Response({'source': "Fetched from TapTapSend API", 'currencies': currencies})
        else:
            return Response({'error': "CAD data not found"}, status=404)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching CAD exchange rates: {e}")
        return Response({'error': "Failed to fetch CAD data from TapTapSend API"}, status=500) 
@api_view(['GET'])
def cad_conversion(request):
    try:
        # Define the API URL and headers
        url = "https://api.taptapsend.com/api/fxRates"
        headers = {
            "appian-version": "web/2022-05-03.0",
            "x-device-id": "web",
            "x-device-model": "web"
        }

        # Extract the currency parameter from the request
        currency_code = request.query_params.get('currency', None)  # E.g., 'PHP', 'USD', etc.

        # Validate that the currency parameter is provided
        if not currency_code:
            return Response({'error': "Currency parameter is required (e.g., ?currency=PHP)"}, status=400)

        # Fetch data from the API
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Filter for CAD exchange rates and the specified currency
        cad_data = next((country for country in data['availableCountries'] if country['currency'] == 'CAD'), None)
        if cad_data:
            currency_data = next((corridor for corridor in cad_data['corridors'] if corridor['currency'] == currency_code), None)
            if currency_data:
                return Response({'source': "Fetched from TapTapSend API", 'data': currency_data})
            else:
                return Response({'error': f"Data for currency '{currency_code}' not found"}, status=404)
        else:
            return Response({'error': "CAD data not found in the API response"}, status=404)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return Response({'error': "Failed to fetch data from TapTapSend API"}, status=500)
