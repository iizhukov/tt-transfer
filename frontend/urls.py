from django.urls import path

from . import views


urlpatterns = [
    path('', views.index),
    path('profile/', views.index),
    path('requests/', views.index),
    path('drivers/', views.index),
    path('crm/', views.index),
    path('cars/', views.index),
    path('tariffs/', views.index),

    path('password-sent/', views.index),
    path('reset-password/', views.index),
    path('register/', views.index),
    path('login/', views.index)
]