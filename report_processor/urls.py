from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('weekly-report/', include('weekly_reports.urls')),
    path('individual-report/', include('individual_reports.urls')),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
