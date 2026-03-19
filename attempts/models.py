from django.db import models
from django.conf import settings
from quizzes.models import Quiz
from quizzes.models import Question
# Create your models here.

User= settings.AUTH_USER_MODEL

class Attempt(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    quiz= models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score= models.IntegerField(default=0)
    started_at= models.DateTimeField(auto_now_add=True)
    completed_at= models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.quiz}"

class Answer(models.Model):
    attempt= models.ForeignKey(Attempt, related_name='answers', on_delete=models.CASCADE)
    question= models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer= models.CharField(max_length=255)
    is_correct= models.BooleanField()

    def __str__(self):
        return f"{self.question} - {self.selected_answer}"
