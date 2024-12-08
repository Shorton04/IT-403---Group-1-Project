from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<int:project_id>/', views.view_project, name='view_project'),
    path('create/', views.create_project, name='create_project'),
]

