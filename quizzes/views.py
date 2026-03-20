from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Quiz,Question 
from .serializers import QuizSerializer
from .services import generate_questions
from rest_framework.throttling import UserRateThrottle
# Create your views here.

class QuizBurstThrottle(UserRateThrottle):
    scope='quiz_burst'

class CreateQuizView(APIView):
    permission_classes=[IsAuthenticated]

    throttle_classes= [UserRateThrottle, QuizBurstThrottle]

    def post(self,request):
        topic= request.data.get('topic')
        difficulty= request.data.get('difficulty')
        count= request.data.get('question_count')

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

