from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'id', 'task_progress', 'uploaded_by', 'file', 'title',
            'is_signed', 'uploaded_at',
        )
        read_only_fields = ('id', 'uploaded_by', 'is_signed', 'uploaded_at')


class DocumentSignSerializer(serializers.Serializer):
    signature = serializers.CharField()
