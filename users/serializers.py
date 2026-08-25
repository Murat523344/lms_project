from rest_framework import serializers
from users.models import User, Payment
from lms.serializers import CourseSerializer, LessonSerializer


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели платежа."""
    
    user_email = serializers.CharField(source='user.email', read_only=True)
    course_name = serializers.CharField(source='paid_course.name', read_only=True, allow_null=True)
    lesson_name = serializers.CharField(source='paid_lesson.name', read_only=True, allow_null=True)
    payment_url = serializers.CharField(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_email', 'paid_course', 'course_name', 
                  'paid_lesson', 'lesson_name', 'amount', 'stripe_session_id',
                  'stripe_payment_status', 'payment_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'stripe_session_id', 'stripe_payment_status']
