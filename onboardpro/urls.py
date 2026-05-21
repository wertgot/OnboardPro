from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('programs.urls')),
    path('api/v1/', include('instances.urls')),
    path('api/v1/', include('documents.urls')),
    path('api/v1/', include('quizzes.urls')),
    path('api/v1/', include('analytics.urls')),
    path('mobile/v1/', include('mobile_bff.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
