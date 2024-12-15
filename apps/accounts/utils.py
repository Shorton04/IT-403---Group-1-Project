from .models import Notification

def notify_account_activity(sender, recipient, message):
    """
    Notify the recipient of account-related activities initiated by the sender.
    """
    Notification.objects.create(recipient=recipient, sender=sender, message=message)
