from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/', include('api.urls')),
    path('api/admin/', include('myadmin.urls')),
    path('api/business/', include('business.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
