from django.urls import path

from . import views


urlpatterns = [
    path('test/', views.TestView.as_view(), name="calculator__test"),

    path('calculate/', views.CalculatorView.as_view(), name="calculator__calculate"),
    path('search/', views.CalculatorSearchView.as_view(), name="calculator__search"),
]
