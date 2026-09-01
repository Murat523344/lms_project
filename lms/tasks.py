from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from lms.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """
    Отправка писем подписчикам об обновлении курса.
    
    Args:
        course_id: ID курса
    """
    try:
        course = Course.objects.get(id=course_id)
        subscribers = Subscription.objects.filter(course=course).select_related('user')
        
        if not subscribers.exists():
            print(f'Нет подписчиков для курса {course.name}')
            return
        
        subject = f'Обновление курса: {course.name}'
        message = f"""
        Здравствуйте!
        
        Курс "{course.name}" был обновлен.
        
        Перейдите по ссылке для просмотра обновлений:
        http://localhost:8000/api/courses/{course.id}/
        
        С уважением,
        Команда LMS
        """
        
        recipient_list = [sub.user.email for sub in subscribers]
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        
        print(f'Письма отправлены подписчикам курса "{course.name}" (всего: {len(recipient_list)})')
    except Course.DoesNotExist:
        print(f'Курс с ID {course_id} не найден')
