from django.urls import path

from . import views

urlpatterns = [
    path('services/', views.GetServicesView.as_view(), name="get_services"),
    path('edit-prices/<int:tariff_id>/', views.EditTariffPricesView.as_view(), name="edit_tariff_prices"),
    path('price-to-car-class/<int:pk>/', views.PriceToCarClassView.as_view(), name="price_to_car_class"),

    path('tariff/', views.TariffView.as_view(), name="tariff"),
    path('tariff/<int:tariff_id>/', views.TariffView.as_view(), name="tariff_by_id"),

    path('export-tariffs/', views.ExportTariffView.as_view(), name="export_tariffs"),
    path('set-last-update/<int:tariff_id>/', views.SetLastUpdateTariff.as_view(), name="set_last_update"),

    path('tariff/<int:tariff_id>/intercity/city/', views.AddLocationToTariff.as_view(location="city"),
         name="add_city_to_tariff"),
    path('tariff/<int:tariff_id>/intercity/global-address/',
         views.AddLocationToTariff.as_view(location="global_address"), name="add_global_address_to_tariff"),
    path('tariff/<int:tariff_id>/intercity/hub/', views.AddLocationToTariff.as_view(location="hub"),
         name="add_hub_to_tariff"),

    path('tariff/<int:tariff_id>/intercity/city/<int:location_id>/', views.AddLocationToTariff.as_view(location="city"),
         name="add_city_to_tariff"),
    path('tariff/<int:tariff_id>/intercity/global-address/<int:location_id>/',
         views.AddLocationToTariff.as_view(location="global_address"), name="add_global_address_to_tariff"),
    path('tariff/<int:tariff_id>/intercity/hub/<int:location_id>/', views.AddLocationToTariff.as_view(location="hub"),
         name="add_hub_to_tariff"),
]
