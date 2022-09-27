from django.urls import path

from . import views


urlpatterns = [
    path("tariff", views.TariffFilterView.as_view(), name="tariff_filter"),
]
