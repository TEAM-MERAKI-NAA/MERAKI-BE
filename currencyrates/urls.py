from django.urls import path
from .views import all_exchange_rates, fetch_cad_exchange_rates, fetch_cad_available_currencies, cad_conversion

urlpatterns = [

    path('api/', all_exchange_rates, name='currency-rates'),
    path('api/CAD/', fetch_cad_exchange_rates, name='fetch-cad-exchange-rates'),
    path('api/exchange-rate/', cad_conversion, name='fetch-exchange-rate-by-currency'),  
    path('api/exchange-rate/', cad_conversion, name='fetch-exchange-rate-by-currency'),  
    path('api/cad-currencies/', fetch_cad_available_currencies, name='fetch-cad-available-currencies'),
]
