from django.urls import path

from . import views


urlpatterns = [
    path('get-news/', views.get_news),
    path('get-news/<int:number>', views.get_news),
]
