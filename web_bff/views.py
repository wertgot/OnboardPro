from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import RoleChoices
from instances.models import OnboardingInstance, TaskProgress
from instances.services import task_due_date
from programs.models import OnboardingStage


class InstanceDetailBFFView(APIView):
    """GET /api/v1/instances/{id}/ — aggregated BFF payload for web client."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            instance = OnboardingInstance.objects.select_related(
                'employee__profile', 'program'
            ).get(pk=pk, program__company=request.user.company)
        except OnboardingInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.role == RoleChoices.EMPLOYEE and instance.employee_id != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        employee = instance.employee
        profile = getattr(employee, 'profile', None)
        progress_map = {
            tp.task_id: tp
            for tp in TaskProgress.objects.filter(instance=instance).select_related('task')
        }

        stages_data = []
        for stage in OnboardingStage.objects.filter(program=instance.program).prefetch_related('tasks'):
            tasks_data = []
            for task in stage.tasks.all():
                tp = progress_map.get(task.id)
                due = task_due_date(instance, task)
                tasks_data.append({
                    'id': task.id,
                    'title': task.title,
                    'task_type': task.task_type,
                    'is_required': task.is_required,
                    'due_date': due.isoformat(),
                    'is_completed': tp.is_completed if tp else False,
                })
            stages_data.append({
                'id': stage.id,
                'name': stage.name,
                'order': stage.order,
                'tasks': tasks_data,
            })

        return Response({
            'id': instance.id,
            'employee': {
                'id': employee.id,
                'full_name': employee.get_full_name() or employee.username,
                'email': employee.email,
                'department': profile.department if profile else '',
                'position': profile.position if profile else '',
                'start_date': profile.start_date.isoformat() if profile else None,
            },
            'program': {
                'id': instance.program.id,
                'name': instance.program.name,
                'description': instance.program.description,
                'is_active': instance.program.is_active,
            },
            'status': instance.status,
            'progress_percent': instance.progress_percent,
            'started_at': instance.started_at.isoformat(),
            'completed_at': instance.completed_at.isoformat() if instance.completed_at else None,
            'stages': stages_data,
        })
