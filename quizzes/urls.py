from django.urls import path
from .views import CreateQuizView, QuizListView, QuizDetailView, QuizManageView

urlpatterns=[
    path('create/',CreateQuizView.as_view(), name='create_quiz'),
    path('',QuizListView.as_view(), name='quiz_list'),
    path('<int:quiz_id>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('<int:quiz_id>/manage/', QuizManageView.as_view(), name='quiz_manage'),
]