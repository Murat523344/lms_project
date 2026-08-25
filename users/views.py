from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
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


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра платежей."""
    queryset = Payment.objects.all().select_related('user', 'paid_course', 'paid_lesson')
    serializer_class = PaymentSerializer
    filterset_fields = ['paid_course', 'paid_lesson', 'stripe_payment_status']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']


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
        
        # Создаем платеж в Stripe
        try:
            payment_url = create_payment_session(request.user, course)
            
            # Получаем последний созданный платеж
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


class PaymentSuccessView(APIView):
    """Обработка успешной оплаты."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        session_id = request.query_params.get('session_id')
        
        if not session_id:
            return Response(
                {'error': 'Необходимо указать session_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            import stripe
            from django.conf import settings
            stripe.api_key = settings.STRIPE_API_KEY
            
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid':
                payment = Payment.objects.get(stripe_session_id=session_id)
                payment.stripe_payment_status = 'paid'
                payment.save()
                return Response({
                    'message': 'Оплата прошла успешно!',
                    'payment_id': payment.id
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'Оплата не подтверждена'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentCancelView(APIView):
    """Обработка отмены оплаты."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'Оплата отменена'
        }, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Получение пары access/refresh токенов."""
    pass
