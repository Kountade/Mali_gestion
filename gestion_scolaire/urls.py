from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import handler404  # Importez handler404
from application.views import custom_404_view  # Importez votre vue personnalisée

# Associez la vue à la gestion des erreurs 404
handler404 = custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls)
]

urlpatterns += i18n_patterns(
    path('', include('application.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)