from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
# Create a schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation for Your Project",
        terms_of_service="https://your-project-terms.com",
        contact=openapi.Contact(email="your-contact-email@example.com"),
        license=openapi.License(name="MIT License"),
    ),
     public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/', include('users.urls')),
    path('api/', include('posts.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
