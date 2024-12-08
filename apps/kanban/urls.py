from django.urls import path
from . import views

urlpatterns = [
    path('', views.board_list, name='board_list'),
    path('board/<int:pk>/', views.board_detail, name='board_detail'),
]