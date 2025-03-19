import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def get_exchange_rates():
    """Helper function to fetch exchange rates from TapTapSend API"""
    url = "https://api.taptapsend.com/api/fxRates"
    headers = {
        "appian-version": "web/2022-05-03.0",
        "x-device-id": "web",
        "x-device-model": "web"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

@api_view(['GET'])
def fetch_exchange_rates(request):
    """Get all exchange rates"""
    try:
        data = get_exchange_rates()
        logger.info("Successfully fetched exchange rates")
        return Response({
            'status': 'success',
            'message': "Successfully fetched exchange rates",
            'data': data
        })
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching exchange rates: {str(e)}")
        return Response({
            'status': 'error',
            'message': "Failed to fetch data from TapTapSend API",
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(f"Unexpected error in fetch_exchange_rates: {str(e)}")
        return Response({
            'status': 'error',
            'message': "An unexpected error occurred",
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def fetch_cad_exchange_rates(request):
    """Get all CAD exchange rates"""
    try:
        data = get_exchange_rates()
        cad_data = next((country for country in data.get('availableCountries', []) 
                        if country.get('currency') == 'CAD'), None)
        
        if cad_data:
            return Response({
                'status': 'success',
                'message': "Successfully fetched CAD exchange rates",
                'data': cad_data
            })
        
        logger.warning("CAD data not found in API response")
        return Response({
            'status': 'error',
            'message': "CAD data not found",
            'error': "No CAD exchange rates available"
        }, status=status.HTTP_404_NOT_FOUND)

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching CAD exchange rates: {str(e)}")
        return Response({
            'status': 'error',
            'message': "Failed to fetch CAD data",
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(f"Unexpected error in fetch_cad_exchange_rates: {str(e)}")
        return Response({
            'status': 'error',
            'message': "An unexpected error occurred",
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def fetch_cad_to_currency(request, currency_code):
    """Helper function to fetch specific CAD to currency exchange rate"""
    try:
        data = get_exchange_rates()
        cad_data = next((country for country in data.get('availableCountries', []) 
                        if country.get('currency') == 'CAD'), None)
        
        if not cad_data:
            logger.warning("CAD data not found in API response")
            return Response({
                'status': 'error',
                'message': "CAD data not found",
                'error': "No CAD exchange rates available"
            }, status=status.HTTP_404_NOT_FOUND)

        currency_data = next((corridor for corridor in cad_data.get('corridors', []) 
                            if corridor.get('currency') == currency_code), None)
        
        if currency_data:
            return Response({
                'status': 'success',
                'message': f"Successfully fetched CAD to {currency_code} rate",
                'data': currency_data
            })
        
        logger.warning(f"Exchange rate not found for CAD to {currency_code}")
        return Response({
            'status': 'error',
            'message': f"Exchange rate not found for {currency_code}",
            'error': f"No exchange rate available for CAD to {currency_code}"
        }, status=status.HTTP_404_NOT_FOUND)

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching CAD to {currency_code} rate: {str(e)}")
        return Response({
            'status': 'error',
            'message': f"Failed to fetch CAD to {currency_code} rate",
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(f"Unexpected error in fetch_cad_to_currency: {str(e)}")
        return Response({
            'status': 'error',
            'message': "An unexpected error occurred",
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def cad_to_php(request):
    """Get CAD to PHP exchange rate"""
    return fetch_cad_to_currency(request, 'PHP')

@api_view(['GET'])
def cad_to_bdt(request):
    """Get CAD to BDT exchange rate"""
    return fetch_cad_to_currency(request, 'BDT')

@api_view(['GET'])
def cad_to_brl(request):
    """Get CAD to BRL exchange rate"""
    return fetch_cad_to_currency(request, 'BRL')

@api_view(['GET'])
def cad_to_usd(request):
    """Get CAD to USD exchange rate"""
    return fetch_cad_to_currency(request, 'USD')

@api_view(['GET'])
def cad_to_xaf(request):
    """Get CAD to XAF exchange rate"""
    return fetch_cad_to_currency(request, 'XAF')

@api_view(['GET'])
def cad_to_cop(request):
    """Get CAD to COP exchange rate"""
    return fetch_cad_to_currency(request, 'COP')

@api_view(['GET'])
def cad_to_dop(request):
    """Get CAD to DOP exchange rate"""
    return fetch_cad_to_currency(request, 'DOP')

@api_view(['GET'])
def cad_to_egp(request):
    """Get CAD to EGP exchange rate"""
    return fetch_cad_to_currency(request, 'EGP')

@api_view(['GET'])
def cad_to_etb(request):
    """Get CAD to ETB exchange rate"""
    return fetch_cad_to_currency(request, 'ETB')

@api_view(['GET'])
def cad_to_gtq(request):
    """Get CAD to GTQ exchange rate"""
    return fetch_cad_to_currency(request, 'GTQ')

@api_view(['GET'])
def cad_to_gnf(request):
    """Get CAD to GNF exchange rate"""
    return fetch_cad_to_currency(request, 'GNF')

@api_view(['GET'])
def cad_to_htg(request):
    """Get CAD to HTG exchange rate"""
    return fetch_cad_to_currency(request, 'HTG')

@api_view(['GET'])
def cad_to_inr(request):
    """Get CAD to INR exchange rate"""
    return fetch_cad_to_currency(request, 'INR')

@api_view(['GET'])
def cad_to_xof(request):
    """Get CAD to XOF exchange rate"""
    return fetch_cad_to_currency(request, 'XOF')

@api_view(['GET'])
def cad_to_jmd(request):
    """Get CAD to JMD exchange rate"""
    return fetch_cad_to_currency(request, 'JMD')

@api_view(['GET'])
def cad_to_kes(request):
    """Get CAD to KES exchange rate"""
    return fetch_cad_to_currency(request, 'KES')

@api_view(['GET'])
def cad_to_mga(request):
    """Get CAD to MGA exchange rate"""
    return fetch_cad_to_currency(request, 'MGA')

@api_view(['GET'])
def cad_to_mxn(request):
    """Get CAD to MXN exchange rate"""
    return fetch_cad_to_currency(request, 'MXN')

@api_view(['GET'])
def cad_to_mad(request):
    """Get CAD to MAD exchange rate"""
    return fetch_cad_to_currency(request, 'MAD')

@api_view(['GET'])
def cad_to_npr(request):
    """Get CAD to NPR exchange rate"""
    return fetch_cad_to_currency(request, 'NPR')

@api_view(['GET'])
def cad_to_ngn(request):
    """Get CAD to NGN exchange rate"""
    return fetch_cad_to_currency(request, 'NGN')

@api_view(['GET'])
def cad_to_pkr(request):
    """Get CAD to PKR exchange rate"""
    return fetch_cad_to_currency(request, 'PKR')

@api_view(['GET'])
def cad_to_lkr(request):
    """Get CAD to LKR exchange rate"""
    return fetch_cad_to_currency(request, 'LKR')

@api_view(['GET'])
def cad_to_tzs(request):
    """Get CAD to TZS exchange rate"""
    return fetch_cad_to_currency(request, 'TZS')

@api_view(['GET'])
def cad_to_gmd(request):
    """Get CAD to GMD exchange rate"""
    return fetch_cad_to_currency(request, 'GMD')

@api_view(['GET'])
def cad_to_tnd(request):
    """Get CAD to TND exchange rate"""
    return fetch_cad_to_currency(request, 'TND')

@api_view(['GET'])
def cad_to_try(request):
    """Get CAD to TRY exchange rate"""
    return fetch_cad_to_currency(request, 'TRY')

@api_view(['GET'])
def cad_to_ugx(request):
    """Get CAD to UGX exchange rate"""
    return fetch_cad_to_currency(request, 'UGX')

@api_view(['GET'])
def cad_to_vnd(request):
    """Get CAD to VND exchange rate"""
    return fetch_cad_to_currency(request, 'VND')

@api_view(['GET'])
def cad_to_zmw(request):
    """Get CAD to ZMW exchange rate"""
    return fetch_cad_to_currency(request, 'ZMW')
