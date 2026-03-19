from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from attempts.models import Attempt
# Create your views here.

class PerformanceView(APIView):
    permission_classes= [IsAuthenticated]

    def get(self,request):
        user= request.user
        attempts= Attempt.objects.filter(user=user)

        total_quizzes= attempts.count()
        total_score= sum(a.score for a in attempts)

        avg_score= total_score/total_quizzes if total_quizzes>0 else 0

        return Response({
            "total_quizzes": total_quizzes,
            "total_score": total_score,
            "average_score": avg_score
        })
    
class HistoryView(APIView):
    permission_classes= [IsAuthenticated]

    def get(self, request):
        user= request.user
        attempts= Attempt.objects.filter(user=user)

        data=[]

        for attempt in attempts:
            data.append({
                "quiz_topic": attempt.quiz.topic,
                "score": attempt.score,
                "completed_at": attempt.completed_at
            })
        
        return Response(data)
