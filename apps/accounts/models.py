from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings


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


class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_notifications'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notifications'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # Ensure this field exists
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"


