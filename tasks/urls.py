from django.urls import path

from . import views


urlpatterns = [
    path('', views.TaskListView.as_view(), name='tasks_list'),
    path('new-task/', views.TaskCreateView.as_view(), name='create_task'),
    path('update-task/<int:pk>/', views.TaskUpdateView.as_view(), name='update_task'),
    path('delete-task/<int:pk>/', views.TaskDeleteView.as_view(), name='delete_task'),
]
