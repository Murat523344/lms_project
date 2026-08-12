from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """Кастомная команда для загрузки платежей из фикстур."""
    
    help = 'Загружает тестовые платежи из фикстур'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка платежей...')
        
        try:
            call_command('loaddata', 'users/fixtures/payments.json')
            self.stdout.write(self.style.SUCCESS('Платежи успешно загружены!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке: {e}'))
