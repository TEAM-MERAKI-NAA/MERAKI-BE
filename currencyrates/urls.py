from django.urls import path
from .views import fetch_exchange_rates,fetch_cad_exchange_rates

urlpatterns = [
    path('currencyrates', fetch_exchange_rates, name='currency-rates'),
    path('currencyrates/CAD', fetch_cad_exchange_rates, name='fetch-cad-exchange-rates'),
]
