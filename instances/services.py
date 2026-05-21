from datetime import timedelta

from django.utils import timezone

from programs.models import Task

from .models import OnboardingInstance, TaskProgress


def task_due_date(instance: OnboardingInstance, task: Task):
    """Deadline = onboarding start + task.due_days."""
    return instance.started_at + timedelta(days=task.due_days)


def recalculate_progress(instance: OnboardingInstance) -> OnboardingInstance:
    """Recompute progress_percent and status from required tasks."""
    required = TaskProgress.objects.filter(
        instance=instance, task__is_required=True
    ).select_related('task')
    total = required.count()
    if total == 0:
        instance.progress_percent = 100.0
    else:
        done = required.filter(is_completed=True).count()
        instance.progress_percent = round(100.0 * done / total, 1)

    now = timezone.now()
    has_overdue = False
    for tp in TaskProgress.objects.filter(instance=instance, is_completed=False).select_related('task'):
        if task_due_date(instance, tp.task) < now:
            has_overdue = True
            break

    old_status = instance.status

    if instance.progress_percent >= 100.0:
        instance.status = OnboardingInstance.Status.COMPLETED
        if not instance.completed_at:
            instance.completed_at = now
    elif has_overdue:
        instance.status = OnboardingInstance.Status.OVERDUE
        instance.completed_at = None
    else:
        instance.status = OnboardingInstance.Status.IN_PROGRESS
        instance.completed_at = None

    instance.save(update_fields=['progress_percent', 'status', 'completed_at'])

    if (
        instance.status == OnboardingInstance.Status.COMPLETED
        and old_status != OnboardingInstance.Status.COMPLETED
    ):
        from notifications.services import notify_onboarding_completed
        notify_onboarding_completed(instance)

    return instance


def create_instance_progress(instance: OnboardingInstance) -> None:
    """Create TaskProgress rows for every task in the program."""
    tasks = Task.objects.filter(stage__program=instance.program)
    TaskProgress.objects.bulk_create(
        [TaskProgress(instance=instance, task=t) for t in tasks],
        ignore_conflicts=True,
    )
