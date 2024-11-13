from django.core.mail import send_mail
from celery import shared_task
from shop.models import Product  
from datetime import date, timedelta

@shared_task
def discount_11_11():
    """
    Периодическая задача, снижающая цену товаров на 15% 
    каждый 11 ноября, а затем восстанавливает ее 12 ноября.
    """
    today = date.today()
    november_11th = date(today.year, 11, 11)
    november_12th = date(today.year, 11, 12)

    products = Product.objects.all()
    
    current_price = float(product.price)
    discount = float(current_price) * 0.15

    # Применение скидки в 00:00 11 ноября каждого года
    if today == november_11th:
        for product in products:            
            new_price = float(current_price) - discount
            product.price = new_price
            product.save()
            print(f"Цена для товара {product.name} снижена до {product.price}")

    # Возвращение исходной цены в 00:00 12 ноября каждого года
    if today == november_12th:
        for product in products:
            product.price += discount
            product.save()
            print(f"Цена для товара {product.name} восстановлена до {product.price}")

@shared_task
def send_new_year_email(recipient_email, subject, message):
    """
    Отправка письма с помощью Celery.

    Args:
        recipient_email (str): Адрес получателя письма.
        subject (str): Тема письма.
        message (str): Содержимое письма.
    """

    send_mail(
        subject,
        message,
        'kazarian@web365.ru',
        [recipient_email],
        fail_silently=False,
    )

    return f"Письмо отправлено на {recipient_email}"