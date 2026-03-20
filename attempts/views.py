from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Attempt
from quizzes.models import Quiz
from django.utils import timezone
from .models import Answer
from quizzes.models import Question
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class StartAttemptView(APIView):
    permission_classes= [IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['quiz_id'],
        properties={
            'quiz_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ))

    def post(self,request):
        quiz_id= request.data.get("quiz_id")

        try:
            quiz= Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz Not Found"}, status=404)
        
        attempt= Attempt.objects.create(
            user= request.user,
            quiz= quiz
        )

        return Response({
            "attempt_id": attempt.id,
            "message:": "Attempt Started"
        })
    
class SubmitAttemptView(APIView):
    permission_classes= [IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['attempt_id', 'answers'],
        properties={
            'attempt_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'answers': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'question_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'selected_answer': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
        }
    ))

    def post(self,request):
        attempt_id= request.data.get("attempt_id")
        answers= request.data.get("answers")

        try:
            attempt= Attempt.objects.get(id=attempt_id, user=request.user)
        except Attempt.DoesNotExist:
            return Response({"error": "Attempt Not Found"}, status= 404)
        
        if attempt.completed_at is not None:
            return Response({"error": "This attempt has already been submitted"}, status=400)
        score=0

        valid_ques_ids= set(
            attempt.quiz.questions.values_list('id', flat=True)
        )

        for ans in answers:
            question_id= ans.get("question_id")
            selected= ans.get("selected_answer")

            if question_id not in valid_ques_ids:
                return Response({
                    "error": f"Question {question_id} does not belong to this quiz"},
                    status=400
                )
            
            try:
                question= Question.objects.get(id= question_id)
            except Question.DoesNotExist:
                continue

            is_correct= (selected==question.correct_answer)

            if is_correct:
                score+=1

            Answer.objects.create(
                attempt=attempt,
                question=question,
                selected_answer= selected,
                is_correct=is_correct
            )
        
        attempt.score= score
        attempt.completed_at= timezone.now()
        attempt.save()

        return Response({
            "score": score,
            "total": len(answers),
            "message": "Attempt Submitted"
        })