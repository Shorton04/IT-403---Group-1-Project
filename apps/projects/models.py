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
    PRIORITY_CHOICES = [
        ('priority', 'Priority'),
        ('urgent', 'Urgent'),
        ('can_wait', 'Can Wait'),
    ]
    STATUS_CHOICES = [
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='priority')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_do')
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)  # New field
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SharedFile(models.Model):
    file = models.FileField(upload_to='shared_files/')
    uploaded_by = models.ForeignKey(CustomUser, related_name='uploaded_files', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='shared_files', on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name