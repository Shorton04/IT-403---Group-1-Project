from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'message', 'is_read', 'created_at', 'notification_type')
    list_filter = ('is_read', 'notification_type', 'created_at')
    search_fields = ('message', 'recipient__username', 'sender__username')
    readonly_fields = ('created_at',)


admin.site.register(Notification, NotificationAdmin)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'full_name', 'role', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'role']
    search_fields = ['email', 'username', 'full_name']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
