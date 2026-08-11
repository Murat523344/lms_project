from django.db import models


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
        help_text='Введите ссылку на видео'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['created_at']
    
    def __str__(self):
        return f'{self.name} ({self.course.name})'
