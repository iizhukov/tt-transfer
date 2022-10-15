from django.urls import path, include


urlpatterns = [
    path('address/', include('api.address.urls')),
    path('tariffs/', include('api.tariffs.urls')),

    path('activity-feed/', include('api.activityFeed.urls')),
    path('admin/', include('api.adminInterface.urls')),
    path('auth/', include('api.authentication.urls')),

    path('cars/', include('api.cars.urls')),
    path('drivers/', include('api.drivers.urls')),

    path('order/', include('api.orders.urls')),
    path('profile/', include('api.profile.urls')),
    
    path('smart-filter/', include('api.smartFilter.urls')),
    path('calculator/', include('api.calculator.urls')),
]
