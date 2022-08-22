from django.urls import path, include


urlpatterns = [
    path('activity-feed/', include('api.activityFeed.urls')),
    path('address/', include('api.address.urls')),
    path('admin/', include('api.adminInterface.urls')),
    path('auth/', include('api.authentication.urls')),

    path('cars/', include('api.cars.urls')),
    path('drivers/', include('api.drivers.urls')),
    path('order/', include('api.orders.urls')),

    path('profile/', include('api.profile.urls')),
    path('smartFilter/', include('api.smartFilter.urls')),
    path('tariffs/', include('api.tariffs.urls')),
]
