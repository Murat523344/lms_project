from rest_framework import serializers
from lms.models import Course, Lesson, Subscription
from lms.validators import validate_youtube_url


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели подписки."""
    
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели урока с валидацией ссылки."""
    
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'course', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def validate_video_url(self, value):
        """Дополнительная валидация поля video_url."""
        return validate_youtube_url(value)


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курса."""
    
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lessons', 'lessons_count', 
                  'owner', 'is_subscribed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()
    
    def get_is_subscribed(self, obj):
        """Проверка, подписан ли текущий пользователь на курс."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.subscribers.filter(user=request.user).exists()
        return False
