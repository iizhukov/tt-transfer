from django.urls import path

from . import views


urlpatterns = [
    path("managers/", views.AdminManagersView.as_view(), name="admin_managers")
]