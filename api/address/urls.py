from django.urls import path

from . import views


urlpatterns = [
    # Address
    path('', views.AddressView.as_view(), name="addresses"),
    path('add-address/', views.AddAddressView.as_view(), name="add_address"),

    # City
    path('city/', views.CityView.as_view(), name="city"),
    path('city-zones/', views.ZonesView.as_view(), name="zones"),
    path('city-zones/<int:id>', views.EditZoneView.as_view(), name="edit_zone"),
    path('get-city-zone-by-coords/', views.GetZoneByCoordsView.as_view(), name="get_zone_by_address"),

    # Hub
    path('hub/', views.HubView.as_view(), name="hub"),
    path('hub-zones/<int:hub_id>/', views.HubZoneView.as_view(), name="hub_zones"),
    path('edit-hub-zone/<int:zone_id>', views.EditHubZoneView.as_view(), name="edit_hub_zone"),
    path('get-hub-zone-by-coordinates/', views.GetHubZoneByCoordsAndHubView.as_view(), name="get_hub_zone_by_coords"),
]
