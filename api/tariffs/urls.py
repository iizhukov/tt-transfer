from django.urls import path

from . import views


urlpatterns = [
    path('tariff/', views.TariffView.as_view(), name="tariff"),
    path('tariff/<int:tariff_id>/', views.TariffView.as_view(), name="tariff_by_id"),
    path('tariff/<int:tariff_id>/services/', views.TariffServicesView.as_view(), name="tariff_services"),
]
