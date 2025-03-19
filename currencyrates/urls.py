from django.urls import path
from .views import all_exchange_rates, fetch_cad_exchange_rates, cad_conversion

urlpatterns = [

    path('api/', all_exchange_rates, name='currency-rates'),
    path('api/CAD/', fetch_cad_exchange_rates, name='fetch-cad-exchange-rates'),
    path('api/exchange-rate/', cad_conversion, name='fetch-exchange-rate-by-currency'),  
]
