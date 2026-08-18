from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from users.permissions import IsOwnerOrStaff


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


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра платежей."""
    queryset = Payment.objects.all().select_related('user', 'paid_course', 'paid_lesson')
    serializer_class = PaymentSerializer
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']


class CustomTokenObtainPairView(TokenObtainPairView):
    """Получение пары access/refresh токенов."""
    pass
