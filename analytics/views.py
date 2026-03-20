from django.shortcuts import render
from django.db.models import Sum, Avg, Count
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from attempts.models import Attempt
# Create your views here.

class StandardPagination(PageNumberPagination):
    page_size=5

class PerformanceView(APIView):
    permission_classes= [IsAuthenticated]

    def get(self,request):
        stats= Attempt.objects.filter(user=request.user).aggregate(
            total_quizzes=Count('id'),
            total_score=Count('score'),
            average_score=Avg('score')
        )
        return Response({
            "total_quizzes": stats['total_quizzes'] or 0,
            "total_score": stats['total_score']or 0,
            "average_score": round(stats['average_score'],2) if stats['average_score'] else 0
        })
    
class HistoryView(APIView):
    permission_classes= [IsAuthenticated]
    pagination_class= StandardPagination

    def get(self, request):
        attempts= Attempt.objects.filter(user=request.user).select_related('quiz').order_by('started_at')

        paginator= self.pagination_class()
        page= paginator.paginate_queryset(attempts, request)

        data=[]

        for attempt in attempts:
            data.append({
                "attempt_id": attempt.id,
                "quiz_topic": attempt.quiz.topic,
                "score": attempt.score,
                "total_questions": attempt.quiz.question_count,
                "completed_at": attempt.completed_at.strftime("%Y-%m-%d %H:%M") if attempt.completed_at else "In Progress"
            })
        
        return paginator.get_paginated_response(data)
