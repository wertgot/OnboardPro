from django.db import models

from accounts.models import Company


class OnboardingProgram(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class OnboardingStage(models.Model):
    program = models.ForeignKey(
        OnboardingProgram, on_delete=models.CASCADE, related_name='stages'
    )
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.program.name} — {self.name}'


class Task(models.Model):
    class TaskType(models.TextChoices):
        DOCUMENT = 'document', 'Документ'
        QUIZ = 'quiz', 'Тест'
        INFO = 'info', 'Информация'
        CHECKLIST = 'checklist', 'Чеклист'

    stage = models.ForeignKey(OnboardingStage, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    task_type = models.CharField(max_length=20, choices=TaskType.choices)
    due_days = models.PositiveIntegerField(
        help_text='Срок выполнения (дней с начала онбординга)'
    )
    is_required = models.BooleanField(default=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title
