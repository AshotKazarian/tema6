"""
Представления для приложения shop.
"""
import time
import django_filters
from django.urls import reverse
from rest_framework import viewsets, serializers, status
from rest_framework.filters import SearchFilter  # , OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, get_object_or_404, redirect
# для рендеринга шаблонов и получения объектов из базы данных.
from django.core.paginator import Paginator
from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import OrderBy
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, CommentForm
from django.views.decorators.http import require_POST
from .models import Category, Product, Brand, Profile, Comment, Visit
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer

def record_visit(request):
    if request.user.is_authenticated:
        Visit.objects.create(
            user=request.user,
            visit_url=request.path,
            visit_time=timezone.now()
        )

      
def visit_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        visits = Visit.objects.order_by('-visit_time')
        return render(request, 'shop/product/visit_list.html', {'visits': visits}) 
    else:
        return HttpResponse('Данная страница предназначена для персонала.')
        

# Функция отображения товаров на главной странице
def product_list(request, category_slug=None, brand_slug=None):
    """
    Отображает список продуктов.

    Эта функция фильтрует продукты по категории и бренду,
    а также отображает список всех категорий и брендов.
  """
    start_time = time.time()
    category = None
    brand = None
    categories = Category.objects.exclude(name__icontains='test')
    brands = Brand.objects.exclude(name__icontains='test')
    products = Product.objects.filter(available=True).prefetch_related('category', 'brand')
    category_slug = request.GET.get("category", category_slug)
    brand_slug = request.GET.get("brand", brand_slug)
    cache_key = f"product_list_{category_slug}_{brand_slug}"
    cached_data = cache.get(cache_key)

    if cached_data is None:
        products = Product.objects.filter(available=True).prefetch_related('category', 'brand')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        if brand_slug:
            brand = get_object_or_404(Brand, slug=brand_slug)
            products = products.filter(brand=brand)
        cached_data = {
            "category": category,
            "categories": list(categories),  # QuerySet в список
            "brand": brand,
            "brands": list(brands),      
            "products": list(products),   
            "category_slug": category_slug,
            "brand_slug": brand_slug,
        }
        cache.set(cache_key, cached_data, timeout=60 * 15)  # Кэш на 15 минут
    else:
        # Восстанавливаем данные из кэша
        category = cached_data["category"]
        categories = cached_data["categories"]
        brand = cached_data["brand"]
        brands = cached_data["brands"]
        products = cached_data["products"]
        category_slug = cached_data["category_slug"]
        brand_slug = cached_data["brand_slug"]
        
    paginator = Paginator(products, 6)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    record_visit(request) 
    
    context = {
        "category": category,
        "categories": categories,
        "brand": brand,
        "brands": brands,
        "products": products,
        "category_slug": category_slug,
        "brand_slug": brand_slug,
        'page': page,   
    }
    
    
    end_time = time.time()
    print(f"Время выполнения с кэшем: {end_time - start_time:.4f} секунд")
    return render(request, "shop/product/list.html", context)

# Функция отображения одного товара
def product_detail(request, slug):
    """
    Отображает информацию о продукте.

    Эта функция получает информацию о продукте по его slug 
    и отображает ее на странице detail.html.
    """
    start_time = time.time()
    cache_key = f"product_{slug}"
    product = cache.get(cache_key)
    if product is None:
        product = get_object_or_404(Product, slug=slug, available=True)
        cache.set(cache_key, product, timeout=60*15) # Кэш на 15 минут
        
    # Список активных комментариев к этому товару
    comments = product.comments.filter(active=True).order_by('-created')
    # Форма для комментирования пользователями
    form = CommentForm() 
    
    # Получаем товары из той же страны
    similar_products = Product.country_products.get_by_country(product.country).exclude(id=product.id)[:3] 
         
    record_visit(request)   
         
    end_time = time.time()
    print(f"Время выполнения с кэшем: {end_time - start_time:.4f} секунд")
    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            'comments': comments,
            'form': form,
            'similar_products': similar_products,
        }
       )


# API
class ProductFilter(django_filters.FilterSet):
    """
    Фильтр для модели Product.

    Позволяет фильтровать товары по категории, бренду, доступности, 
    а также минимальной и максимальной цене.
    """
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        """
        Метаданные для фильтра.
        
        model:  Указывает, к какой модели применяется фильтр.
        fields:  Указывает, какие поля модели должны быть отфильтрованы.
        """
        model = Product
        fields = ["category", "brand", "available", "min_price", "max_price"]


class ProductPriceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product, 
    используемый для изменения цены.

    Ограничивает цену, чтобы она была не меньше нуля.
    """
    class Meta:
        """
        Метаданные для сериализатора.
        
        model:  Указывает, к какой модели применяется сериализатор.
        fields:  Указывает, какие поля модели должны быть сериализованы.
        """
        model = Product
        fields = ["price"]

    def validate_price(self, value):
        """
        Проверяет, что цена не меньше нуля.
        """
        if value < 0:
            raise serializers.ValidationError("Цена не может быть меньше нуля.")
        return value


class ProductViewSet(viewsets.ModelViewSet):
    """
    API-представление для модели Product.

    Предоставляет CRUD-операции, 
    а также действия для статистики 
     и изменения цены.
     """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]  # , OrderingFilter
    search_fields = ["name", "description"]
    filterset_class = ProductFilter

    @action(methods=["GET"], detail=False)
    def statistics(self, request):
        """
        Сводная статистика.
        """
        all_count = self.get_queryset().count()
        available_count = self.get_queryset().filter(available=True).count()
        unavailable_count = self.get_queryset().filter(available=False).count()
        category_count = (
        self.get_queryset().select_related('category', 'brand').values("category__name").annotate(count=Count("id"))
    )
        brand_count = (
        self.get_queryset().select_related('category', 'brand').values("brand__name").annotate(count=Count("id"))
    )

        return Response(
            {
                "Всего товаров": all_count,
                "В наличии": available_count,
                "Нет в наличии": unavailable_count,
                "Статистика по категориям": category_count,
                "Статистика по брендам": brand_count,
            }
        )

    @action(methods=["GET"], detail=False)
    def sale(self, request):
        """
        Просмотр товаров по акции.
        """
        products_sale1 = Product.objects.filter(
            Q(category__name="Утюги")
            & (Q(brand__name="Philips") | Q(brand__name="Tefal"))
            & ~Q(price__gte=7000)
        )

        products_sale2 = Product.objects.filter(
            Q(updated__gte=timezone.now() - timezone.timedelta(days=2))
            & (
                (Q(category__name="Холодильники") & Q(price__lte=100000))
                | (Q(category__name="Микроволновки") & Q(price__lte=13000))
            )
        )

        # Сериализация объектов Product
        serializer1 = ProductSerializer(products_sale1, many=True)
        serializer2 = ProductSerializer(products_sale2, many=True)

        return Response(
            {
                "Акция 1: Утюги Philips и Tefal не дороже 7000": serializer1.data,
                "Акция 2: Холодильники не дороже 100000 и микроволновки не дороже 13000. \
                Дата обновления товара: последние 2 дня": serializer2.data,
            }
        )

    @action(methods=["POST"], detail=True)
    def change_price(self, request, pk=None):
        """
        Изменяет цену товара.
        """
        product = self.get_object()
        serializer = ProductPriceSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Цена товара изменена."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        """
        Возвращает сериализатор, который нужно использовать для действия "change_price".
        """
        if self.action == "change_price":
            return ProductPriceSerializer
        return super().get_serializer_class()


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API-представление для модели Category.

    Предоставляет CRUD-операции.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class BrandViewSet(viewsets.ModelViewSet):
    """
    API-представление для модели Brand.

    Предоставляет CRUD-операции.
  """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


# CRUD-операции (создание, чтение, обновление, удаление)

# В ProductViewSet вы не пишете эти методы явно, так как они уже определены в ModelViewSet:

# - get (GET):  Получение списка продуктов или одного продукта по ID.
# - post (POST): Создание нового продукта.
# - put (PUT): Обновление существующего продукта.
# - delete (DELETE): Удаление продукта по ID.

# 1. get:
# - Если запрос содержит pk (ID продукта), метод retrieve (получение по ID) будет вызван,
# и вы получите один продукт.
# - Если pk отсутствует, будет вызван метод list (получение списка), и вы получите список
# всех продуктов.
# 2. post: Метод create (создание) вызывается для создания нового продукта, используя
# данные из request.data.
# 3. put: Метод update (обновление) вызывается для обновления существующего продукта с pk.
# 4. delete: Метод destroy (удаление) вызывается для удаления продукта с pk.

def user_login(request):
    record_visit(request) 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session.set_expiry(600)
                    return redirect('shop:product_list')
                else:
                    return HttpResponse('Профиль не активен.')
            else:
                return HttpResponse('Неверные логин или пароль.')
    else:
        form = LoginForm()
    return render(request, 'shop/product/login.html', {'form': form})
    
def user_logout(request):
    record_visit(request) 
    logout(request)
    return redirect('shop:login')

def register(request):
    record_visit(request) 
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object using the cleaned data from the form
            new_user = User(
                username=user_form.cleaned_data['username'],
                first_name=user_form.cleaned_data['first_name'],
            )
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = Profile(user=new_user)
            profile.first_name = user_form.cleaned_data['first_name']
            profile.save()

            return redirect('shop:login')
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'shop/product/register.html',
                  {'user_form': user_form})

@require_POST
def product_comment(request, slug):
    record_visit(request) 
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Пожалуйста, авторизуйтесь.')

    product = get_object_or_404(Product, slug=slug)
    comment = None
    # A comment was posted
    form = CommentForm(request.POST, request.FILES)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.product = product
        comment.name = request.user.get_full_name()
        # Save the comment to the database
        comment.save()
    return redirect('shop:product_detail', slug=product.slug)

def edit_comment(request, comment_id):
    record_visit(request) 
    comment = get_object_or_404(Comment, id=comment_id)
    #Проверка является ли пользователь автором комментария
    if request.user.get_full_name() != comment.name:
        return HttpResponseForbidden("Вы не можете редактировать чужие комментарии.")
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('shop:product_detail', slug=comment.product.slug)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'shop/edit_comment.html', {'form': form, 'comment': comment})

def submit_edit_comment(request, comment_id):
    record_visit(request) 
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)
    #Проверка является ли пользователь автором комментария
        if request.user.get_full_name() != comment.name:
            return HttpResponseForbidden("Вы не можете редактировать чужие комментарии.")
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
        return redirect(reverse('shop:product_detail', kwargs={'slug': comment.product.slug}))
    else:
        return HttpResponseForbidden("Доступ запрещен")
        
def delete_comment(request, comment_id):
    record_visit(request) 
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.get_full_name() != comment.name:
      return HttpResponseForbidden("Вы не можете удалять чужие комментарии.")
    if request.method == 'POST':
      comment.delete()
      return redirect('shop:product_detail', slug=comment.product.slug)
    else:
      return HttpResponseForbidden("Доступ запрещен")
