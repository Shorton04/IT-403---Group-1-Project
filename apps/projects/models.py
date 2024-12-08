from django.db import models
from django.conf import settings
from django.utils.timezone import now

from apps.accounts.models import CustomUser

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField(default=now)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_projects')
    members = models.ManyToManyField(CustomUser, related_name='assigned_projects')
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name