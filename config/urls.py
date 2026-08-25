from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка документации
schema_view = get_schema_view(
    openapi.Info(
        title="LMS API",
        default_version='v1',
        description="Документация для LMS системы",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@lms.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def root_view(request):
    """Корневой маршрут с информацией о API."""
    return JsonResponse({
        'message': 'Добро пожаловать в LMS систему!',
        'endpoints': {
            'admin': '/admin/',
            'api_courses': '/api/courses/',
            'api_lessons': '/api/lessons/',
            'api_users': '/api/users/',
            'api_payments': '/api/users/payments/',
            'api_subscriptions': '/api/subscriptions/',
            'api_docs': '/swagger/',
            'api_redoc': '/redoc/',
        }
    })


urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include('lms.urls')),
    path('api/users/', include('users.urls')),
    
    # Документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
