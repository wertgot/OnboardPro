from django.db import models
from django.utils import timezone

from accounts.models import User
from programs.models import OnboardingProgram, Task


class OnboardingInstance(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'В процессе'
        COMPLETED = 'completed', 'Завершён'
        OVERDUE = 'overdue', 'Просрочен'

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='onboarding_instances')
    program = models.ForeignKey(OnboardingProgram, on_delete=models.CASCADE, related_name='instances')
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.IN_PROGRESS
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percent = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.employee} — {self.program.name}'


class TaskProgress(models.Model):
    instance = models.ForeignKey(
        OnboardingInstance, on_delete=models.CASCADE, related_name='progress'
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('instance', 'task')

    def __str__(self):
        return f'{self.task.title} ({self.instance_id})'

    def save(self, *args, **kwargs):
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed:
            self.completed_at = None
        super().save(*args, **kwargs)
