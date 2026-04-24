from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    path('assets/<path:path>', serve, {
        'document_root': settings.BASE_DIR / 'frontend' / 'dist' / 'assets',
    }),
    path('', include('core.urls')),
]
