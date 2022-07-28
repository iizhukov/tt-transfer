from django.urls import path

from . import views


urlpatterns = [
    path('city/', views.CityView.as_view(), name="city"),
]