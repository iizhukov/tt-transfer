from django.urls import path

from . import views


urlpatterns = [
    path('user-car/', views.UserCarView.as_view(), name="user_car"),
    path('get-car-classes/', views.GetCarClassesView.as_view(), name="get_car_classes")
]
