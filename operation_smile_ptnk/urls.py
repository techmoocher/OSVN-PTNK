"""URL configuration for the Operation Smile PTNK project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('activities/', include(('activities.urls', 'activities'), namespace='activities')),
    path('', include(('pages.urls', 'pages'), namespace='pages')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'pages.views.custom_404'