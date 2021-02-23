from django.urls import path

from . import views


urlpatterns = [
    path('', views.WeeklyReportView.as_view(), name='weekly_report'),
]
