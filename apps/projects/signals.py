from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from apps.notifications.models import Notification

@receiver(post_save, sender=Task)
def create_task_notification(sender, instance, created, **kwargs):
    if created:
        message = f"You have been assigned a new task: {instance.name}"
        Notification.objects.create(user=instance.assigned_to, task=instance, message=message)