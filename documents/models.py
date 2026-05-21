from django.conf import settings
from django.db import models

from instances.models import TaskProgress


class Document(models.Model):
    task_progress = models.ForeignKey(
        TaskProgress, on_delete=models.CASCADE, related_name='documents'
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents'
    )
    file = models.FileField(upload_to='documents/%Y/%m/')
    title = models.CharField(max_length=255, blank=True)
    is_signed = models.BooleanField(default=False)
    signature = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.file.name
