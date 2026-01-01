from django.urls import path, include
from .views import QuizCreateView, QuizViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')

urlpatterns = [
    path('', include(router.urls)),
    path('createQuiz/', QuizCreateView.as_view(), name='quiz-create'),
]