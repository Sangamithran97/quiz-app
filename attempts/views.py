from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Attempt
from quizzes.models import Quiz
from django.utils import timezone
from .models import Answer
from quizzes.models import Question
# Create your views here.

class StartAttemptView(APIView):
    permission_classes= [IsAuthenticated]

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

    def post(self,request):
        attempt_id= request.data.get("attempt_id")
        answers= request.data.get("answers")

        try:
            attempt= Attempt.objects.get(id=attempt_id, user=request.user)
        except Attempt.DoesNotExist:
            return Response({"error": "Attempt Not Found"}, status= 404)
        
        score=0

        for ans in answers:
            question_id= ans.get("question_id")
            selected= ans.get("selected_answer")
            
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