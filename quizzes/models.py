from django.db import models
from django.conf import settings
# Create your models here.
User= settings.AUTH_USER_MODEL

class Quiz(models.Model):
    topic= models.CharField(max_length=255)
    difficulty= models.CharField(max_length=50)
    question_count= models.IntegerField()
    created_by= models.ForeignKey(User, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} ({self.difficulty})"
    
class Question(models.Model):
    quiz=models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text= models.TextField()
    options= models.JSONField()
    correct_answer= models.CharField(max_length=255)

    def __str__(self):
        return self.question_text
    