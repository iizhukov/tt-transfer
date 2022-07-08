from django.urls import path

from . import views


urlpatterns = [
    path('news-list/', views.NewsListView.as_view(), name='news_list'),
]
