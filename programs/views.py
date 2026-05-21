from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.models import RoleChoices
from onboardpro.permissions import IsHR

from .models import OnboardingProgram, OnboardingStage, Task
from .serializers import (
    OnboardingProgramDetailSerializer,
    OnboardingProgramSerializer,
    OnboardingStageSerializer,
    TaskSerializer,
)


class OnboardingProgramViewSet(viewsets.ModelViewSet):
    serializer_class = OnboardingProgramSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['is_active']

    def get_queryset(self):
        return OnboardingProgram.objects.filter(
            company=self.request.user.company
        ).prefetch_related('stages__tasks')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OnboardingProgramDetailSerializer
        return OnboardingProgramSerializer

    def get_permissions(self):
        if self.request.user.role == RoleChoices.EMPLOYEE:
            return [IsAuthenticated()]
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsHR()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


class OnboardingStageViewSet(viewsets.ModelViewSet):
    serializer_class = OnboardingStageSerializer
    permission_classes = [IsHR]

    def get_queryset(self):
        return OnboardingStage.objects.filter(
            program__company=self.request.user.company
        ).prefetch_related('tasks')


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsHR]

    def get_queryset(self):
        return Task.objects.filter(
            stage__program__company=self.request.user.company
        )
