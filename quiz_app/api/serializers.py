from rest_framework import serializers
from ..models import Quiz, Question
from django.contrib.auth import get_user_model

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for Question objects.
    Handles validation and serialization of Question data.
    """
    class Meta:
        model = Question
        fields = ['id',
                  'question_title',
                  'question_options',
                  'answer',
                  ]


class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for Quiz objects.
    Handles validation and serialization of Quiz data.
    """
    url = serializers.URLField(source='video_url', write_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 
                  'title',
                  'description',
                  'created_at', 
                  'updated_at',
                  'url',
                  'video_url',
                  'questions']
        read_only_fields = ['video_url']


# URL = 'https://www.youtube.com/watch?v=BaW_jenozKc'