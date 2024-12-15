from django.contrib import admin
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'deadline', 'created_by', 'created_at')
    list_filter = ('created_by', 'deadline')
    search_fields = ('name', 'description')
    list_select_related = ('created_by',)  # To optimize queries and include related "created_by" field

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'assigned_to', 'priority', 'status', 'deadline', 'created_at')
    list_filter = ('project', 'priority', 'status')
