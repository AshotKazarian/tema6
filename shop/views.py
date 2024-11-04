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
    
    
    


    return render(request,
                  'shop/product/detail.html',
                  {'product': product,})


# API
from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer 
from rest_framework.filters import SearchFilter #, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
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
    def statistics(self, request):
        """Сводная статистика."""
        all_count = self.get_queryset().count()
        available_count = self.get_queryset().filter(available=True).count()
        unavailable_count = self.get_queryset().filter(available=False).count()
        category_count = self.get_queryset().values('category__name').annotate(count=Count('id'))
        brand_count = self.get_queryset().values('brand__name').annotate(count=Count('id'))

        return Response({
      'Всего товаров': all_count,
      'В наличии': available_count,
      'Нет в наличии': unavailable_count,
      'Статистика по категориям': category_count,
      'Статистика по брендам': brand_count,
    })
    
    @action(methods=['GET'], detail=False)
    def sale(self, request):

        category_sale1 = get_object_or_404(Category, name='Утюги')
        brand_sale11 = get_object_or_404(Brand, name='Philips')
        brand_sale12 = get_object_or_404(Brand, name='Tefal')
        products_sale1 = Product.objects.filter( Q(category=category_sale1) & 
        (Q(brand=brand_sale11) | Q(brand=brand_sale12)) &~
        Q(price__gte=7000) )
  
    
        category_sale21 = get_object_or_404(Category, name='Холодильники')
        category_sale22 = get_object_or_404(Category, name='Микроволновки')
        products_sale2 = Product.objects.filter( Q(created__gte=timezone.now() - timezone.timedelta(days=1)) &
        ((Q(category=category_sale21) & Q(price__lte=100000)) |
        (Q(category=category_sale22) & Q(price__lte=13000)))
        )
    
    # Сериализация объектов Product
        serializer1 = ProductSerializer(products_sale1, many=True)
        serializer2 = ProductSerializer(products_sale2, many=True)

        return Response({
              'Акция 1: Утюги Philips и Tefal не дороже 7000': serializer1.data,
              'Акция 2: Холодильники не дороже 100000 и микроволновки не дороже 13000. Дата добавления товара: последние 2 дня': serializer2.data
    })
         
         
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
    
          