from rest_framework import serializers

from .models import OnboardingProgram, OnboardingStage, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id', 'stage', 'title', 'task_type', 'due_days',
            'is_required', 'content',
        )


class OnboardingStageSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = OnboardingStage
        fields = ('id', 'program', 'name', 'order', 'tasks')


class OnboardingProgramSerializer(serializers.ModelSerializer):
    stages_count = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = OnboardingProgram
        fields = (
            'id', 'name', 'description', 'is_active',
            'stages_count', 'tasks_count', 'created_at',
        )
        read_only_fields = ('id', 'created_at', 'stages_count', 'tasks_count')

    def get_stages_count(self, obj):
        return obj.stages.count()

    def get_tasks_count(self, obj):
        return Task.objects.filter(stage__program=obj).count()


class OnboardingProgramDetailSerializer(OnboardingProgramSerializer):
    stages = OnboardingStageSerializer(many=True, read_only=True)

    class Meta(OnboardingProgramSerializer.Meta):
        fields = OnboardingProgramSerializer.Meta.fields + ('stages',)
