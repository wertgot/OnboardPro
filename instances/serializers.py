from rest_framework import serializers

from .models import OnboardingInstance, TaskProgress


class OnboardingInstanceSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(write_only=True)
    program_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OnboardingInstance
        fields = (
            'id', 'employee', 'employee_id', 'program', 'program_id',
            'status', 'started_at', 'completed_at', 'progress_percent',
        )
        read_only_fields = (
            'id', 'employee', 'program', 'status', 'started_at',
            'completed_at', 'progress_percent',
        )


class TaskProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskProgress
        fields = ('id', 'instance', 'task', 'is_completed', 'completed_at', 'notes')
        read_only_fields = ('id', 'instance', 'task', 'completed_at')
