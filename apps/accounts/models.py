from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, default='profile_pictures/default-profile.jpg')
    role_choices = [
        ('project_manager', 'Project Manager'),
        ('project_member', 'Project Member'),
    ]
    role = models.CharField(max_length=20, choices=role_choices, default='project_manager')
    full_name = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='members')  # Links to Project Manager

    def generate_member_id(self):
        """Generates a unique Member ID linked to the Project Manager's ID."""
        if self.created_by:
            return f"{self.created_by.id}-{uuid.uuid4().hex[:8]}"
        return uuid.uuid4().hex[:8]
