from django.urls import path

from . import views


urlpatterns = [
    path('user-car/', views.UserCarView.as_view(), name="user_car"),
]
