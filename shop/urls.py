from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'shop' 

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('brands', views.BrandViewSet)
router.register('categories', views.CategoryViewSet) 

urlpatterns = [
    path('', views.product_list, name='product_list'), 
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'), 
    path('brand/<slug:brand_slug>/', views.product_list, name='product_list_by_brand'), 
    path('api/', include(router.urls)),  # Маршрут для API
    path('<slug:slug>/', views.product_detail, name='product_detail'),  # Детальная страница
]

# router.urls  уже содержит маршруты для  products, brands и categories, которые 
# автоматически определяют первичный ключ (<pk>) в URL-адресах.