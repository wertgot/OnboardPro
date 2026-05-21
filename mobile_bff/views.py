from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import RoleChoices
from instances.models import OnboardingInstance, TaskProgress
from instances.services import recalculate_progress, task_due_date


class MyTasksView(APIView):
    """GET /mobile/v1/my-tasks/ — compact task list for mobile."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role not in (RoleChoices.EMPLOYEE, RoleChoices.HR, RoleChoices.ADMIN):
            return Response([])

        status_filter = request.query_params.get('status')
        qs = TaskProgress.objects.filter(
            instance__employee=request.user,
            instance__status__in=[
                OnboardingInstance.Status.IN_PROGRESS,
                OnboardingInstance.Status.OVERDUE,
            ],
        ).select_related('task', 'instance')

        if status_filter == 'pending':
            qs = qs.filter(is_completed=False)
        elif status_filter == 'done':
            qs = qs.filter(is_completed=True)

        today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        result = []
        for tp in qs:
            due = task_due_date(tp.instance, tp.task)
            urgent = (not tp.is_completed) and (due <= today_end)
            result.append({
                'id': tp.task_id,
                'progress_id': tp.id,
                'title': tp.task.title,
                'type': tp.task.task_type,
                'due': due.isoformat(),
                'done': tp.is_completed,
                'urgent': urgent,
            })
        return Response(result)


class MyTaskPatchView(APIView):
    """PATCH /mobile/v1/my-tasks/{id}/ — mark task done (task id)."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        done = request.data.get('done', request.data.get('is_completed'))
        if done is None:
            return Response({'detail': 'Поле done обязательно.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tp = TaskProgress.objects.select_related('instance').get(
                task_id=pk,
                instance__employee=request.user,
            )
        except TaskProgress.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        tp.is_completed = bool(done)
        tp.save()
        recalculate_progress(tp.instance)
        due = task_due_date(tp.instance, tp.task)
        today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        return Response({
            'id': tp.task_id,
            'title': tp.task.title,
            'type': tp.task.task_type,
            'due': due.isoformat(),
            'done': tp.is_completed,
            'urgent': (not tp.is_completed) and (due <= today_end),
        })
