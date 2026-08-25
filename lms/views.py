from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from lms.permissions import IsModerator, IsOwner, IsOwnerOrModerator
from lms.paginators import CoursePaginator, LessonPaginator


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Course с правами доступа."""
    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    """Представление для списка уроков и создания нового урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class SubscriptionView(APIView):
    """Представление для управления подпиской на курс."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        
        if not course_id:
            return Response(
                {'error': 'Необходимо указать course_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        course = get_object_or_404(Course, id=course_id)
        
        subscription = Subscription.objects.filter(user=user, course=course)
        
        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
            is_subscribed = False
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'
            is_subscribed = True
        
        return Response({
            'message': message,
            'is_subscribed': is_subscribed,
            'course_id': course.id,
            'course_name': course.name
        }, status=status.HTTP_200_OK)
