from rest_framework import viewsets, generics
from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Course.
    Предоставляет CRUD операции: list, create, retrieve, update, destroy.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateView(generics.ListCreateAPIView):
    """Представление для списка уроков и создания нового урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
