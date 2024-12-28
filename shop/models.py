"""
Этот модуль содержит модели для django проекта.

Он определяет модели:
    - Category (категория товаров)
    - Brand (бренд товаров)
    - Product (товар)
"""

from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Модель для представления категории товаров.

    Атрибуты:
        name (CharField): Название категории.
        slug (SlugField): Уникальный URL-идентификатор категории.
    """

    name = models.CharField(max_length=200, verbose_name="Название", unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    history = HistoricalRecords()

    class Meta:
        """
        Мета-информация для модели Category.
        """
        
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        """
        Возвращает строковое представление объекта Category.
        """
        return str(self.name)

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для страницы детализации категории.
        """
        return reverse("shop:product_list_by_category", args=[self.slug])


class Brand(models.Model):
    """
    Модель для представления бренда товаров.

    Атрибуты:
        name (CharField): Название бренда.
        slug (SlugField): Уникальный URL-идентификатор бренда.
    """

    name = models.CharField(max_length=200, verbose_name="Название", unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    history = HistoricalRecords()

    class Meta:
        """
        Мета-информация для модели Brand.
        """
          
        ordering = ["name"]  
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        """
        Возвращает строковое представление объекта Brand.
        """
        return str(self.name)

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для страницы детализации бренда.
        """
        return reverse("shop:product_list_by_brand", args=[self.slug])

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('category', 'brand')

class CountryProductManager(models.Manager):
    def get_by_country(self, country_code):
        return self.get_queryset().filter(country=country_code).select_related('category', 'brand')

class Product(models.Model):
    """
    Модель для представления товара.

    Атрибуты:
        category (ForeignKey): Категория, к которой относится товар.
        brand (ForeignKey): Бренд товара.
        name (CharField): Название товара.
        slug (SlugField): Уникальный URL-идентификатор товара.
        image (ImageField): Изображение товара.
        description (TextField): Описание товара.
        price (DecimalField): Цена товара.
        available (BooleanField): Доступность товара.
        created (DateTimeField): Дата создания товара.
        updated (DateTimeField): Дата обновления товара.
    """
    
    class Country(models.TextChoices):
        Russia = 'RU', 'Россия'
        Germany = 'GE', 'Германия'
        Japan = 'JP', 'Япония'
        ND = 'ND', 'Нет данных'
        
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )
    brand = models.ForeignKey(
        Brand, related_name="products", on_delete=models.CASCADE, verbose_name="Бренд"
    )
    name = models.CharField(max_length=200, verbose_name="Название", unique=True)
    slug = models.SlugField(max_length=200, verbose_name="Метка", unique=True)
    image = models.ImageField(
        upload_to="products/%Y/%m/%d", blank=True, verbose_name="Изображение"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Цена")
    available = models.BooleanField(default=True, verbose_name="Наличие")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания товара"
    )
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления товара")
    history = HistoricalRecords()
    country = models.CharField(max_length=2,
        choices=Country.choices,
        default=Country.ND,
        verbose_name="Страна производства")
        
    objects = ProductManager() #базовый менеджер
    country_products = CountryProductManager() #менеджер для товаров по стране

    class Meta:
        """
        Мета-информация для модели Product.
        """
        
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        """
        Возвращает строковое представление объекта Product.
        """
        return str(self.name)

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для страницы детализации товара.
        """
        return reverse("shop:product_detail", args=[self.slug])
        
    @property
    def country_name(self):
        """
        Возвращает название страны производства товара.
        """
        return self.get_country_display()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)

class Comment(models.Model):
    product = models.ForeignKey(Product,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField(verbose_name="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Comment by {self.name} on {self.product}"
        
