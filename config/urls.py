from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


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
        }
    })


urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include('lms.urls')),
    path('api/users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
