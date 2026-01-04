from django.db import models
from django.contrib.auth import get_user_model

class Quiz(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, default='')
    description = models.TextField(null=False, blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField(null=False, blank=False, default='')
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_title = models.CharField(max_length=255, null=False, blank=False, default='')
    question_options = models.JSONField() 
    answer = models.CharField(max_length=255, null=False, blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_title