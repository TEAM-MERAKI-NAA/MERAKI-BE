from django.urls import path
from .views import (
    all_exchange_rates,
    fetch_cad_exchange_rates,
    fetch_cad_available_currencies,
    cad_conversion
)

urlpatterns = [
    path('exchange-rates/', all_exchange_rates, name='all-exchange-rates'),
    path('exchange-rates/cad/', fetch_cad_exchange_rates, name='cad-exchange-rates'),
    path('exchange-rates/cad/currencies/', fetch_cad_available_currencies, name='cad-currencies'),
    path('exchange-rates/cad/conversion/', cad_conversion, name='cad-currency-conversion'),
]
