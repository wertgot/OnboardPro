from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TaskProgress
from .services import recalculate_progress


@receiver(post_save, sender=TaskProgress)
def on_task_progress_saved(sender, instance, **kwargs):
    recalculate_progress(instance.instance)
