from django.urls import path, include


urlpatterns = [
    path('auth/', include('api.authentication.urls')),
    path('profile/', include('api.profiles.urls')),
    path('activity-feed/', include('api.activityFeed.urls')),
    path('cars/', include('api.cars.urls')),
    path('drivers/', include('api.drivers.urls')),
]
