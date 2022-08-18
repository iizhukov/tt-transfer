from django.urls import path

from . import views


urlpatterns = [
    path('', views.AddressView.as_view(), name="addresses"),
    path('city/', views.CityView.as_view(), name="city"),
    path('add/', views.AddAddressView.as_view(), name="add_address"),
    path('zones/', views.ZonesView.as_view(), name="zones"),
    path('zones/<int:id>', views.EditZoneView.as_view(), name="edit_zone"),
    path('get-zone-by-coords/', views.GetZoneByCoordsView.as_view(), name="get_zone_by_address"),
    path('hub/', views.HubView.as_view(), name="hub")
]
