from django.contrib import admin
from django.urls import path, include
from azbankgateways.urls import az_bank_gateways_urls


urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('account/', include('account.urls')),
    path('comment/', include('comment.urls')),
    path('apiadmin/', include('api_admin.urls')),
    path('', include('django.contrib.auth.urls')),
    path('products/', include('E_commerce.urls')),
    path("bankgateways/", az_bank_gateways_urls()),
    path('api-auth/', include('rest_framework.urls')),
]




from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
