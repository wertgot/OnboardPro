from django.contrib import admin

from .models import OnboardingProgram, OnboardingStage, Task


class StageInline(admin.TabularInline):
    model = OnboardingStage
    extra = 0


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


@admin.register(OnboardingProgram)
class OnboardingProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'is_active', 'created_at')
    inlines = [StageInline]


@admin.register(OnboardingStage)
class OnboardingStageAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'order')
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'stage', 'task_type', 'due_days', 'is_required')
