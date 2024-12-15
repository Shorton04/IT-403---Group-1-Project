from apps.accounts.models import Notification

def notify_project_activity(sender, recipient, project, message):
    """
    Notify the recipient of project-related activities initiated by the sender.
    """
    Notification.objects.create(recipient=recipient, sender=sender, message=message, notification_type='project_activity')
