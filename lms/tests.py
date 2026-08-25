from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from lms.models import Course, Lesson, Subscription


class LessonTests(TestCase):
    """Тесты для CRUD операций с уроками."""
    
    def setUp(self):
        """Подготовка тестовых данных."""
        # Создаем пользователей
        self.user = User.objects.create_user(
            email='user@example.com',
            password='test123'
        )
        self.moderator_user = User.objects.create_user(
            email='moderator@example.com',
            password='test123'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='test123'
        )
        
        # Создаем группу модераторов
        moderator_group, _ = Group.objects.get_or_create(name='Модератор')
        self.moderator_user.groups.add(moderator_group)
        
        # Создаем курс
        self.course = Course.objects.create(
            name='Тестовый курс',
            description='Описание курса',
            owner=self.user
        )
        
        # Создаем урок (владелец - self.user)
        self.lesson = Lesson.objects.create(
            name='Тестовый урок',
            description='Описание урока',
            video_url='https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )
        
        # Клиенты для API
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.moderator_client = APIClient()
        self.moderator_client.force_authenticate(user=self.moderator_user)
        self.other_client = APIClient()
        self.other_client.force_authenticate(user=self.other_user)
    
    def test_create_lesson_success(self):
        """Тест успешного создания урока."""
        url = reverse('lesson-list-create')
        data = {
            'name': 'Новый урок',
            'description': 'Описание нового урока',
            'video_url': 'https://www.youtube.com/watch?v=new',
            'course': self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
    
    def test_create_lesson_invalid_url(self):
        """Тест создания урока с невалидной ссылкой."""
        url = reverse('lesson-list-create')
        data = {
            'name': 'Новый урок',
            'description': 'Описание нового урока',
            'video_url': 'https://vk.com/video/test',
            'course': self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Разрешены только ссылки на youtube.com', str(response.data))
    
    def test_create_lesson_moderator_forbidden(self):
        """Тест: модератор не может создать урок."""
        url = reverse('lesson-list-create')
        data = {
            'name': 'Урок модератора',
            'description': 'Описание',
            'video_url': 'https://www.youtube.com/watch?v=test',
            'course': self.course.id
        }
        response = self.moderator_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_lesson_owner_success(self):
        """Тест: владелец может обновить урок."""
        url = reverse('lesson-detail', args=[self.lesson.id])
        data = {'name': 'Обновленный урок'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Обновленный урок')
    
    def test_update_lesson_moderator_success(self):
        """Тест: модератор может обновить урок."""
        url = reverse('lesson-detail', args=[self.lesson.id])
        data = {'name': 'Обновлено модератором'}
        response = self.moderator_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Обновлено модератором')
    
    def test_update_lesson_other_user_forbidden(self):
        """Тест: другой пользователь не может обновить урок."""
        url = reverse('lesson-detail', args=[self.lesson.id])
        data = {'name': 'Попытка взлома'}
        response = self.other_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_lesson_owner_success(self):
        """Тест: владелец может удалить урок."""
        url = reverse('lesson-detail', args=[self.lesson.id])
        response = self.client.delete(url)
        # Проверяем, что владелец может удалить
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
    
    def test_delete_lesson_moderator_forbidden(self):
        """Тест: модератор не может удалить урок."""
        url = reverse('lesson-detail', args=[self.lesson.id])
        response = self.moderator_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_lesson_other_user_forbidden(self):
        """Тест: другой пользователь не может удалить урок."""
        url = reverse('lesson-detail', args=[self.lesson.id])
        response = self.other_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTests(TestCase):
    """Тесты для работы с подписками."""
    
    def setUp(self):
        """Подготовка тестовых данных."""
        self.user = User.objects.create_user(
            email='user@example.com',
            password='test123'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='test123'
        )
        
        self.course = Course.objects.create(
            name='Тестовый курс',
            description='Описание курса',
            owner=self.user
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.other_client = APIClient()
        self.other_client.force_authenticate(user=self.other_user)
    
    def test_subscribe_success(self):
        """Тест успешного создания подписки."""
        url = reverse('subscription')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(response.data['is_subscribed'])
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
    
    def test_unsubscribe_success(self):
        """Тест успешного удаления подписки."""
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)
        
        url = reverse('subscription')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(response.data['is_subscribed'])
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
    
    def test_subscribe_no_course_id(self):
        """Тест: ошибка при отсутствии course_id."""
        url = reverse('subscription')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Необходимо указать course_id', str(response.data))
    
    def test_subscribe_invalid_course(self):
        """Тест: ошибка при несуществующем курсе."""
        url = reverse('subscription')
        data = {'course_id': 999}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_subscribe_other_user(self):
        """Тест: другой пользователь может подписаться на курс."""
        url = reverse('subscription')
        data = {'course_id': self.course.id}
        response = self.other_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.other_user, course=self.course).exists())
    
    def test_course_is_subscribed_field(self):
        """Тест: поле is_subscribed в сериализаторе курса."""
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)
        
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что поле is_subscribed есть и равно True
        self.assertTrue(response.data['results'][0]['is_subscribed'])
        
        # Проверяем для другого пользователя
        response = self.other_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['results'][0]['is_subscribed'])
