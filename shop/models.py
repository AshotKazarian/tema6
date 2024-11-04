from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название",
                            unique=True)
    slug = models.SlugField(max_length=200,
                            unique=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

class Brand(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название",
                            unique=True)
    slug = models.SlugField(max_length=200,
                            unique=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('shop:product_list_by_brand',
                       args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE, 
                                 verbose_name="Категория")
    brand = models.ForeignKey(Brand,
                                 related_name='products',
                                 on_delete=models.CASCADE, 
                                 verbose_name="Бренд")                             
    name = models.CharField(max_length=200, 
                                 verbose_name="Название",
                                 unique=True)
    slug = models.SlugField(max_length=200, 
                                 verbose_name="Метка", 
                                 unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True, 
                                 verbose_name="Изображение")
    description = models.TextField(blank=True, 
                                 verbose_name="Описание")
    price = models.DecimalField(max_digits=10,
                                decimal_places=0, 
                                 verbose_name="Цена")
    available = models.BooleanField(default=True, 
                                 verbose_name="Наличие")
    created = models.DateTimeField(auto_now_add=True, 
                                 verbose_name="Дата создания товара")
    updated = models.DateTimeField(auto_now=True, 
                                 verbose_name="Дата обновления товара")
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.slug])
                                             
                                             