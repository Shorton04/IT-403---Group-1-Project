from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('/register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('/logout/', views.logout_view, name='logout'),
    path('/profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path('register-member/', views.register_member_view, name='register_member'),
    path('member_list/', views.member_list, name='member_list'),
    path('edit_member/<int:user_id>/', views.edit_member, name='edit_member'),
    path('delete_member/<int:user_id>/', views.delete_member, name='delete_member'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)