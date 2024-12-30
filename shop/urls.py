"""
URLs для приложения shop.
"""

from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from . import views

SchemaView = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

app_name = "shop"

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("brands", views.BrandViewSet)
router.register("categories", views.CategoryViewSet)

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("category/<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    path("brand/<slug:brand_slug>/", views.product_list, name="product_list_by_brand"),
    path("api/", include(router.urls)),
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('<slug:slug>/comment/', views.product_comment, name='product_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('submit_edit_comment/<int:comment_id>/', views.submit_edit_comment, name='submit_edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('visits/', views.visit_list, name='visit_list'),
    path("<slug:slug>/", views.product_detail, name="product_detail"),
]

# router.urls  уже содержит маршруты для  products, brands и categories, которые
# автоматически определяют первичный ключ (<pk>) в URL-адресах.
