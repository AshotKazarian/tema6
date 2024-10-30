from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Brand
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer


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

    return render(request,
                  'shop/product/detail.html',
                  {'product': product})


# API
from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer 
from rest_framework.filters import SearchFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer 
    filter_backends = [SearchFilter]
    search_fields = ['name']
    
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer 
    filter_backends = [SearchFilter]
    search_fields = ['name']
    

from rest_framework.filters import SearchFilter
