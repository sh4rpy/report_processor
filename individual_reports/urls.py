from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndividualReportView.as_view(), name='individual_report'),
]
