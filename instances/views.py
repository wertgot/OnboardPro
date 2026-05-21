from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import RoleChoices, User
from onboardpro.permissions import IsHR, IsOwnerOrHR
from programs.models import OnboardingProgram

from .models import OnboardingInstance, TaskProgress
from .serializers import OnboardingInstanceSerializer, TaskProgressSerializer
from .services import create_instance_progress, recalculate_progress


class OnboardingInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = OnboardingInstanceSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        from web_bff.views import InstanceDetailBFFView
        return InstanceDetailBFFView().get(request, pk=kwargs['pk'])

    def get_queryset(self):
        qs = OnboardingInstance.objects.filter(
            program__company=self.request.user.company
        ).select_related('employee', 'program')
        if self.request.user.role == RoleChoices.EMPLOYEE:
            return qs.filter(employee=self.request.user)
        return qs

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsHR()]
        if self.request.user.role == RoleChoices.EMPLOYEE:
            return [IsAuthenticated()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        employee_id = request.data.get('employee_id')
        program_id = request.data.get('program_id')
        if not employee_id or not program_id:
            return Response(
                {'detail': 'employee_id и program_id обязательны.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            employee = User.objects.get(
                pk=employee_id, company=request.user.company
            )
            program = OnboardingProgram.objects.get(
                pk=program_id, company=request.user.company
            )
        except (User.DoesNotExist, OnboardingProgram.DoesNotExist):
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)

        instance = OnboardingInstance.objects.create(employee=employee, program=program)
        create_instance_progress(instance)
        recalculate_progress(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskProgressViewSet(viewsets.GenericViewSet):
    """PATCH /api/v1/instances/{id}/tasks/{tid}/"""

    serializer_class = TaskProgressSerializer
    permission_classes = [IsOwnerOrHR]

    def get_task_progress(self, instance_id, task_id):
        return TaskProgress.objects.select_related(
            'instance__employee', 'task'
        ).get(
            instance_id=instance_id,
            task_id=task_id,
            instance__program__company=self.request.user.company,
        )

    def partial_update(self, request, instance_pk=None, pk=None):
        if request.user.role == RoleChoices.EMPLOYEE:
            tp = self.get_task_progress(instance_pk, pk)
            if tp.instance.employee_id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            tp = self.get_task_progress(instance_pk, pk)

        serializer = self.get_serializer(tp, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
