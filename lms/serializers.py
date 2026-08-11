from rest_framework import serializers
from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели урока."""
    
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'course', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курса."""
    
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lessons', 'lessons_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
