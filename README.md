# LMS Project — Система онлайн-обучения

## Описание

Бэкенд-приложение LMS для онлайн-обучения на Django REST Framework.

## Технологии

- Python 3.11
- Django 6 + DRF
- PostgreSQL 15
- Redis 7
- Celery + Celery Beat
- Docker + Docker Compose

## Быстрый старт

### 1. Клонирование

    git clone https://github.com/Murat523344/lms_project.git
    cd lms_project

### 2. Создание .env

    cp .env.template .env

Отредактируйте .env (особенно SECRET_KEY и TELEGRAM_BOT_TOKEN).

### 3. Запуск всех сервисов

    docker-compose up -d --build

### 4. Миграции и суперпользователь

    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser

### 5. Доступ

- Админка: http://localhost:8000/admin/
- Swagger: http://localhost:8000/swagger/
- Redoc: http://localhost:8000/redoc/
- API курсов: http://localhost:8000/api/courses/
- API уроков: http://localhost:8000/api/lessons/

## Управление

    docker-compose logs -f        логи
    docker-compose down           остановка
    docker-compose down -v        остановка + удаление данных
    docker-compose restart        перезапуск

## Сервисы

| Сервис      | Описание   | Порт          |
|-------------|------------|---------------|
| web         | Django     | 8000          |
| db          | PostgreSQL | 5432 (expose) |
| redis       | Redis      | 6379 (expose) |
| celery      | Worker     | -             |
| celery-beat | Beat       | -             |

## Автор

Мурат — студент Skypro

## Контакты

Email: support@lms.local
