from django.conf import settings
from django.db import models

from programs.models import Task


class Quiz(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=255)
    pass_score = models.PositiveIntegerField(default=70, help_text='Минимальный % для зачёта')

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    score = models.FloatField(default=0.0)
    passed = models.BooleanField(default=False)
    answers = models.JSONField(default=dict)
    attempted_at = models.DateTimeField(auto_now_add=True)
