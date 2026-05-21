from django.contrib import admin

from .models import OnboardingInstance, TaskProgress


class TaskProgressInline(admin.TabularInline):
    model = TaskProgress
    extra = 0


@admin.register(OnboardingInstance)
class OnboardingInstanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'program', 'status', 'progress_percent', 'started_at')
    inlines = [TaskProgressInline]


@admin.register(TaskProgress)
class TaskProgressAdmin(admin.ModelAdmin):
    list_display = ('instance', 'task', 'is_completed', 'completed_at')
