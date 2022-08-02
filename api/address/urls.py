from django.urls import path

from . import views


urlpatterns = [
    path('', views.AddressView.as_view(), name="addresses"),
    path('city/', views.CityView.as_view(), name="city"),
    path('add/', views.AddAddressView.as_view(), name="add_address"),
    path('zones/', views.ZonesView.as_view(), name="zones"),
]
