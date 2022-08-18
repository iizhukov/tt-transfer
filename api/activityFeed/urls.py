from django.urls import path

from . import views


urlpatterns = [
    path('', views.NewsView.as_view(), name='news_list'),
    path('images/<int:id>/', views.NewsImageView.as_view(), name="images"),
    path('files/<int:id>/', views.NewsFileView.as_view(), name="files"),
]
