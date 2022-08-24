from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('map/', include('map.urls')),
    # re_path(r'^cml/', include('cml.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
