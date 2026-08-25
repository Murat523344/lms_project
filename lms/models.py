from django.db import models
from django.conf import settings


class Course(models.Model):
    """Модель курса."""
    
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название курса'
    )
    preview = models.ImageField(
        upload_to='courses/previews/',
        blank=True,
        null=True,
        verbose_name='Превью (картинка)'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание курса'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='Владелец',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель урока."""
    
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название урока'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание урока'
    )
    preview = models.ImageField(
        upload_to='lessons/previews/',
        blank=True,
        null=True,
        verbose_name='Превью (картинка)'
    )
    video_url = models.URLField(
        verbose_name='Ссылка на видео',
        help_text='Введите ссылку на видео (только youtube.com)'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Владелец',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['created_at']
    
    def __str__(self):
        return f'{self.name} ({self.course.name})'


class Subscription(models.Model):
    """Модель подписки на обновления курса."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Курс'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'course')  # Гарантия уникальности пары
    
    def __str__(self):
        return f'{self.user.email} - {self.course.name}'
