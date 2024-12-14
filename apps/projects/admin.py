from django.contrib import admin
from .models import Project, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'assigned_to', 'priority', 'status', 'deadline', 'created_at')
    list_filter = ('project', 'priority', 'status')
