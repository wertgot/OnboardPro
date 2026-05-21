from rest_framework import serializers

from .models import AnswerOption, Question, Quiz, QuizAttempt


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ('id', 'text')
        read_only_fields = fields


class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'order', 'options')


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ('id', 'task', 'title', 'pass_score', 'questions')


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ('id', 'quiz', 'user', 'score', 'passed', 'attempted_at')
        read_only_fields = ('id', 'user', 'score', 'passed', 'attempted_at')


class QuizAttemptCreateSerializer(serializers.Serializer):
    """answers: {question_id: option_id}"""

    answers = serializers.DictField(child=serializers.IntegerField())
