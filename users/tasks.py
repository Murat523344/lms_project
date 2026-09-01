from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def deactivate_inactive_users():
    """
    Блокировка пользователей, которые не заходили более месяца.
    """
    one_month_ago = timezone.now() - timedelta(days=30)
    
    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True,
        is_staff=False,
        is_superuser=False
    )
    
    count = inactive_users.count()
    
    if count > 0:
        inactive_users.update(is_active=False)
        print(f'Заблокировано {count} неактивных пользователей')
    else:
        print('Неактивных пользователей не найдено')
    
    return {'blocked_count': count}
