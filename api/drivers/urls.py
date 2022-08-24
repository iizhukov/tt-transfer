from django.urls import path

from . import views


urlpatterns = [
    path("driver/", views.DriverView.as_view(), name="driver"),
    path("driver/<int:id>/", views.DriverView.as_view(), name="driver_by_id")
]
