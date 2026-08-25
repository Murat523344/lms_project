import re
from rest_framework.exceptions import ValidationError


def validate_youtube_url(value):
    """
    Валидатор для проверки, что ссылка ведет на youtube.com.
    
    Args:
        value: URL для проверки
    
    Raises:
        ValidationError: Если ссылка не ведет на youtube.com
    """
    # Паттерн для проверки youtube ссылок
    youtube_pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/'
    
    if not re.match(youtube_pattern, value):
        raise ValidationError(
            'Разрешены только ссылки на youtube.com'
        )
    
    return value
