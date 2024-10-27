
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('imgs/', include('galeria.urls')),
    path('streamfield/', include('streamfield.urls')),
    path('componentes/', include('streamblocks.urls')),
    path('comments/', include('django_comments.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
        )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
        )
