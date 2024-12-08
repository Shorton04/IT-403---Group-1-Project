from django.shortcuts import render, redirect
from .models import Notification

def notification_list(request):
    notifications = Notification.objects.filter(user=request.user, read=False)
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

def mark_as_read(request, pk):
    notification = Notification.objects.get(pk=pk, user=request.user)
    notification.read = True
    notification.save()
    return redirect('notification_list')