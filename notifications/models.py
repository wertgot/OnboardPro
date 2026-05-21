from django.conf import settings
from django.db import models


class Notification(models.Model):
    class Channel(models.TextChoices):
        EMAIL = 'email', 'Email'

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications'
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    channel = models.CharField(max_length=20, choices=Channel.choices, default=Channel.EMAIL)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sent_at']
