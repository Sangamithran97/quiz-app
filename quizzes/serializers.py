from rest_framework import serializers
from .models import Quiz, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Question
        fields= ['id', 'question_text', 'options']

class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Quiz
        fields= ['id', 'topic', 'difficulty', 'question_count', 'created_at']

class QuizSerializer(serializers.ModelSerializer):
    questions= QuestionSerializer(many=True, read_only=True)
    class Meta:
        model=Quiz
        fields='__all__'