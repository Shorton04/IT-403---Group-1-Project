from django.urls import path
from . import views
from .views import kanban_board, update_task_status

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('create/', views.create_project, name='create_project'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('project/<int:project_id>/kanban/', kanban_board, name='kanban_board'),
    path('update_task_status/', update_task_status, name='update_task_status'),
    path('projects/<int:project_id>/tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/update-status/', views.update_task_status, name='update_task_status'),


]

