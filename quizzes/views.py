from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Quiz,Question 
from .serializers import QuizSerializer, QuizListSerializer
from .services import generate_questions
from rest_framework.throttling import UserRateThrottle
from accounts.permissions import IsAdmin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class QuizBurstThrottle(UserRateThrottle):
    scope='quiz_burst'

class CreateQuizView(APIView):
    permission_classes=[IsAuthenticated]

    throttle_classes= [UserRateThrottle, QuizBurstThrottle]

    @swagger_auto_schema(request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['topic', 'difficulty', 'question_count'],
            properties={
                'topic': openapi.Schema(type=openapi.TYPE_STRING),
                'difficulty': openapi.Schema(type=openapi.TYPE_STRING),
                'question_count': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
    ))

    def post(self,request):
        topic= request.data.get('topic')
        difficulty= request.data.get('difficulty')
        count= request.data.get('question_count')

        VALID_DIFFICULTIES = ['easy', 'medium', 'hard']

        if not topic or not difficulty or not count:
            return Response({"error": "topic, difficulty and question_count are required"}, status=400)
        if difficulty not in VALID_DIFFICULTIES:
            return Response({"error": "difficulty must be easy, medium or hard"}, status=400)
        if not isinstance(count, int) or count < 1 or count > 20:
            return Response({"error": "question_count must be between 1 and 20"}, status=400)

        questions_data= generate_questions(topic, difficulty, count)

        if not questions_data:
            return Response({
                "error": "Failed to generate Questions. Please try again later."},
                status= status.HTTP_503_SERVICE_UNAVAILABLE
            )

        quiz= Quiz.objects.create(
            topic=topic,
            difficulty=difficulty,
            question_count= count,
            created_by= request.user
        )

        for q in questions_data:
            Question.objects.create(
                quiz= quiz,
                question_text= q['question_text'],
                options= q['options'],
                correct_answer= q['correct_answer']
            )

        serializer= QuizSerializer(quiz)
        return Response(serializer.data)

class QuizListView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        quizzes= Quiz.objects.all().order_by('-created_at')
        serializer= QuizListSerializer(quizzes, many=True)
        return Response(serializer.data)

class QuizDetailView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, quiz_id):
        try:
            quiz= Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status =404)
        serializer= QuizSerializer(quiz)
        return Response(serializer.data)
    
class QuizManageView(APIView):
    permission_classes = [IsAdmin]

    @swagger_auto_schema(operation_description="Admin only - delete a quiz")
    def delete(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=404)
        quiz.delete()
        return Response({"message": "Quiz deleted successfully"}, status=204)