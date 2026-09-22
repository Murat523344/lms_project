from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from users.permissions import IsOwnerOrStaff
from users.services import create_payment_session


class UserCreateView(generics.CreateAPIView):
    """Регистрация нового пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(generics.ListAPIView):
    """Список пользователей (только для админов)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, редактирование и удаление пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrStaff]


class PaymentListView(generics.ListAPIView):
    """Список платежей."""
    queryset = Payment.objects.all().select_related('user', 'paid_course', 'paid_lesson')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentCreateView(APIView):
    """Создание платежа и получение ссылки на оплату."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {'error': 'Необходимо указать course_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from lms.models import Course
        course = get_object_or_404(Course, id=course_id)

        if not course.price:
            return Response(
                {'error': 'Для этого курса не указана цена'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            create_payment_session(request.user, course)
            payment = Payment.objects.filter(
                user=request.user,
                paid_course=course,
                stripe_payment_status='pending'
            ).latest('created_at')
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': f'Ошибка при создании платежа: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    """Получение пары access/refresh токенов."""
    pass
