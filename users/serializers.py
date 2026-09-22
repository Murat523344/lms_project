from rest_framework import serializers
from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'telegram_chat_id',
                  'password', 'date_joined']
        read_only_fields = ['id', 'date_joined']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели платежа."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    course_name = serializers.CharField(source='paid_course.name',
                                        read_only=True, allow_null=True)
    lesson_name = serializers.CharField(source='paid_lesson.name',
                                        read_only=True, allow_null=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_email', 'paid_course', 'course_name',
                  'paid_lesson', 'lesson_name', 'amount', 'stripe_session_id',
                  'stripe_payment_status', 'payment_url',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at',
                            'stripe_session_id', 'stripe_payment_status']
