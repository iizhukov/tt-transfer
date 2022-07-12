from django.urls import path, include


urlpatterns = [
    path('auth/', include('api.authentication.urls')),
    path('activity-feed/', include('api.activityFeed.urls')),
    path('cars/', include('api.cars.urls')),
    path('managers/', include('api.manager.urls')),
]
