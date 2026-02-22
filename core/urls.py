from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="VisionTech API",
        default_version='v1',
        description="API REST pour le site VisionTech - Formations, Services, Réalisations et Contact",
        terms_of_service="https://visiontech.vision/terms/",
        contact=openapi.Contact(email="contact@visiontech.vision"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/formations/', include('apps.formations.urls')),
    path('api/v1/services/', include('apps.services.urls')),
    path('api/v1/realisations/', include('apps.realisations.urls')),
    path('api/v1/contact/', include('apps.contact.urls')),
    
    # Documentation Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
