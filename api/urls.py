from django.urls import path, include


urlpatterns = [
    path('auth/', include('api.authentication.urls')),
    path('activity-feed/', include('api.activityFeed.urls')),
]
