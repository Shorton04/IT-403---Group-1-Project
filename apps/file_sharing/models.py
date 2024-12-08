from django.db import models
from django.conf import settings

class SharedFile(models.Model):
    file = models.FileField(upload_to='shared_files/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shared_files')

    def __str__(self):
        return self.file.name