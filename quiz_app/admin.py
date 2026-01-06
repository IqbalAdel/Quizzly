from django.contrib import admin
from .models import Quiz

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creator', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'creator__username')
    list_filter = ('created_at', 'updated_at')
