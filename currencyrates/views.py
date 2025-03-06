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
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "appian-version": "web/2022-05-03.0",
            "origin": "https://www.taptapsend.com",
            "referer": "https://www.taptapsend.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "x-device-id": "web",
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