from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Quiz,Question 
from .serializers import QuizSerializer
from .services import generate_questions
# Create your views here.

class CreateQuizView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        topic= request.data.get('topic')
        difficulty= request.data.get('difficulty')
        count= request.data.get('question_count')

        quiz= Quiz.objects.create(
            topic=topic,
            difficulty=difficulty,
            question_count= count,
            created_by= request.user
        )

        questions_data= generate_questions(topic, difficulty, count)

        for q in questions_data:
            Question.objects.create(
                quiz= quiz,
                question_text= q['question_text'],
                options= q['options'],
                correct_answer= q['correct_answer']
            )

        serializer= QuizSerializer(quiz)
        return Response(serializer.data)

