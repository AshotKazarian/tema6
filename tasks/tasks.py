from celery import shared_task
from shop.models import Product  

@shared_task
def increase_product_price():
        """
        ТЕСТ
        Периодическая задача, увеличивающая цену товара на 
        5 каждые 15 секунд для товаров с брендом (id=1).
        """
        products = Product.objects.filter(brand="3")
        for product in products:
            current_price = product.price
            new_price = current_price + 5
            product.price = new_price
            product.save()
            print(f"Цена для товара {product.name} изменена на {product.price}")