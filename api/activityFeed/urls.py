from django.urls import path

from . import views


urlpatterns = [
    path('', views.NewsView.as_view(), name='news_list'),
    path('<int:limit>', views.NewsView.as_view(), name='news_list'),
    path('images/', views.NewsImageView.as_view(), name="images"),
    path('files/', views.NewsFileView.as_view(), name="files"),
]
