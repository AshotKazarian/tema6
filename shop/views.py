from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Brand
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from django.db.models import Q
from django.utils import timezone


# Функция отображения товаров на главной странице
def product_list(request, category_slug=None, brand_slug=None):
    category = None
    brand = None
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(available=True)

    category_slug = request.GET.get('category', category_slug)
    brand_slug = request.GET.get('brand', brand_slug)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    else:
        # Если category_slug не задан, значит нам нужны все категории
        category = None

    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(brand=brand)
    else:
        # Если brand_slug не задан, значит нам нужны все бренды
        brand = None

    paginator = Paginator(products, 9)

    page = request.GET.get('page') # Получаем номер текущей страницы
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Если номер страницы не целое число, показываем первую страницу
        products = paginator.page(1)
    except EmptyPage:
        # Если номер страницы превышает максимальное число страниц, 
        # показываем последнюю страницу
        products = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'categories': categories,
        'brand': brand,
        'brands': brands,
        'products': products,
        'category_slug': category_slug, 
        'brand_slug': brand_slug,
        'page': page,                 # Добавляем page в контекст
    }
    return render(request, 'shop/product/list.html', context)

# Функция отображения одного товара
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    
    
    # Q запросы
    category_sale1 = get_object_or_404(Category, name='Утюги')
    brand_sale11 = get_object_or_404(Brand, name='Philips')
    brand_sale12 = get_object_or_404(Brand, name='Tefal')
    products_sale1 = Product.objects.filter( Q(category=category_sale1) & 
    (Q(brand=brand_sale11) | Q(brand=brand_sale12)) &~
    Q(price__gte=7000) )
  
    
    category_sale21 = get_object_or_404(Category, name='Холодильники')
    category_sale22 = get_object_or_404(Category, name='Микроволновки')
    products_sale2 = Product.objects.filter( Q(created__gte=timezone.now() - timezone.timedelta(days=2)) &
    Q(category=category_sale21) & Q(price__lte=100000) |
    Q(category=category_sale22) & Q(price__lte=13000))


    return render(request,
                  'shop/product/detail.html',
                  {'product': product, 
                  'products_sale1': products_sale1,
                  'products_sale2': products_sale2})


# API
from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer 
from rest_framework.filters import SearchFilter #, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from random import choice
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

class ProductFilter(django_filters.FilterSet):
  min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
  max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

  class Meta:
    model = Product
    fields = ['category', 'brand', 'available', 'min_price', 'max_price']
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    filter_backends = [SearchFilter, DjangoFilterBackend] # , OrderingFilter
    search_fields = ['name', 'description']
    filterset_class = ProductFilter
    
    @action(methods=['GET'], detail=False)
    def available(self, request):
        """Товары в наличии."""
        available_products = self.get_queryset().filter(available=True)
        serializer = self.get_serializer(available_products, many=True)
        return Response(serializer.data)
        
    @action(methods=['GET'], detail=False)
    def unavailable(self, request):
        """Товары не в наличии."""
        unavailable_products = self.get_queryset().filter(available=False)
        serializer = self.get_serializer(unavailable_products, many=True)
        return Response(serializer.data)        
    


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer 
    filter_backends = [SearchFilter]
    search_fields = ['name']
    
    @action(methods=['GET'], detail=True)
    def random_product(self, request, pk=None):
        """Случайный товар из выбранной категории."""
        category = self.get_object() 
        products = category.products.all()
        if products.exists():
            random_product = choice(products)
            serializer = ProductSerializer(random_product)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Нет товаров выбранной категории'}, status=404)
     
    @action(methods=['POST'], detail=True)
    def update_category_info(self, request, pk=None):
        """Обновление данных категории"""
        category = self.get_object()
        name = request.data.get('name')
        slug = request.data.get('slug')
        category.name = name
        category.slug = slug


        category.save()
        return Response({'detail': 'Информация о категории обновлена'}, status=200)
    
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer 
    filter_backends = [SearchFilter]
    search_fields = ['name']
    
    @action(methods=['GET'], detail=True)
    def random_product(self, request, pk=None):
        """Случайный товар из выбранного бренда."""
        brand = self.get_object() 
        products = brand.products.all()
        if products.exists():
            random_product = choice(products)
            serializer = ProductSerializer(random_product)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Нет товаров выбранного бренда'}, status=404)
            
    @action(methods=['POST'], detail=True)
    def update_brand_info(self, request, pk=None):
        """Обновление данных бренда"""
        brand = self.get_object()
        name = request.data.get('name')
        slug = request.data.get('slug')
        brand.name = name
        brand.slug = slug


        brand.save()
        return Response({'detail': 'Информация о бренде обновлена'}, status=200)