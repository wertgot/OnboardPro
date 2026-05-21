from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import RoleChoices
from onboardpro.permissions import IsHR

from .models import AnswerOption, Quiz, QuizAttempt
from .serializers import (
    QuizAttemptCreateSerializer,
    QuizAttemptSerializer,
    QuizSerializer,
)


class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(
            task__stage__program__company=self.request.user.company
        ).prefetch_related('questions__options')

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsHR()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'], url_path='attempt')
    def attempt(self, request, pk=None):
        quiz = self.get_object()
        serializer = QuizAttemptCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answers = serializer.validated_data['answers']

        total = quiz.questions.count()
        correct = 0
        for q in quiz.questions.all():
            chosen = answers.get(str(q.id)) or answers.get(q.id)
            if chosen and AnswerOption.objects.filter(
                question=q, id=chosen, is_correct=True
            ).exists():
                correct += 1

        score = round(100.0 * correct / total, 1) if total else 0.0
        passed = score >= quiz.pass_score
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            user=request.user,
            score=score,
            passed=passed,
            answers=answers,
        )
        return Response(QuizAttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)


class QuizAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = QuizAttempt.objects.filter(
            quiz__task__stage__program__company=self.request.user.company
        )
        if self.request.user.role == RoleChoices.EMPLOYEE:
            return qs.filter(user=self.request.user)
        return qs
