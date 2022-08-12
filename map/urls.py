from django.urls import path

from . import views


urlpatterns = [
    path('zones/', views.zones, name="map_zones"),
    path('route/', views.route, name="map_route")
]