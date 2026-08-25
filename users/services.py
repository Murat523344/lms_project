import stripe
from django.conf import settings
from users.models import Payment


stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(course):
    """
    Создание продукта в Stripe.
    
    Args:
        course: Объект курса
    
    Returns:
        ID созданного продукта в Stripe
    """
    product = stripe.Product.create(
        name=course.name,
        description=course.description,
    )
    return product.id


def create_stripe_price(amount, product_id):
    """
    Создание цены в Stripe.
    
    Args:
        amount: Сумма в рублях
        product_id: ID продукта в Stripe
    
    Returns:
        ID созданной цены в Stripe
    """
    price = stripe.Price.create(
        unit_amount=int(amount * 100),  # Перевод в копейки
        currency='rub',
        product=product_id,
    )
    return price.id


def create_stripe_session(price_id, success_url, cancel_url):
    """
    Создание сессии для оплаты в Stripe.
    
    Args:
        price_id: ID цены в Stripe
        success_url: URL для успешной оплаты
        cancel_url: URL для отмены оплаты
    
    Returns:
        Объект сессии Stripe
    """
    session = stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
    )
    return session


def create_payment_session(user, course):
    """
    Создание полной сессии оплаты.
    
    Args:
        user: Объект пользователя
        course: Объект курса
    
    Returns:
        Ссылка на оплату
    """
    # Создаем продукт в Stripe
    product_id = create_stripe_product(course)
    
    # Создаем цену в Stripe
    price_id = create_stripe_price(course.price, product_id)
    
    # Создаем сессию оплаты
    success_url = 'http://localhost:8000/api/users/payments/success/'
    cancel_url = 'http://localhost:8000/api/users/payments/cancel/'
    session = create_stripe_session(price_id, success_url, cancel_url)
    
    # Сохраняем платеж в базе данных
    payment = Payment.objects.create(
        user=user,
        paid_course=course,
        amount=course.price,
        stripe_session_id=session.id,
        stripe_payment_status='pending',
        payment_url=session.url,
    )
    
    return session.url
