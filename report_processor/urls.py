from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('weekly-report/', include('weekly_reports.urls')),
    path('individual_report/', include('individual_reports.urls')),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
