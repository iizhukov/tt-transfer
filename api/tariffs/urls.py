from django.urls import path

from . import views


urlpatterns = [
    path('intracity-tariff/', views.IntracityTariffView.as_view(), name="intracity_tariff"),
]
