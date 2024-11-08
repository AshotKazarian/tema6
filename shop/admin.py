"""
Этот модуль реализует админ-панель для django проекта.
"""

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from .models import Category, Brand, Product


class ProductResource(resources.ModelResource):
    """
    Ресурс для экспорта данных о товарах.

    Этот класс предоставляет возможность экспортировать данные о товарах в
    различных форматах, таких как CSV, JSON, XLSX и др.

    Атрибуты:
        model: Модель Product, которая будет использоваться для экспорта.
        fields: Список полей, которые будут включены в экспорт.

    Методы:
        dehydrate_price(self, obj): Форматирует цену товара с точностью
        до двух знаков после запятой.

        dehydrate_description(self, instance): Возвращает описание товара
        или "Описание отсутствует", если оно не задано.

        dehydrate_available(self, obj): Возвращает строку "Есть в наличии"
        или "Нет в наличии" в зависимости от значения атрибута available.
    """

    class Meta:
        """
        Настройки для экспорта данных о товарах.

        Атрибуты:
            model: Модель Product, которая будет использоваться для экспорта.
            fields: Список полей, которые будут включены в экспорт.
        """

        model = Product
        fields = (
            "id",
            "name",
            "price",
            "brand__name",
            "category__name",
            "available",
            "description",
            "created",
            "updated",
        )

    def dehydrate_price(self, obj):
        """
        Форматирует цену объекта для вывода.
        Строка с форматированной ценой, округлённой до двух знаков после запятой.
        """
        return f"{obj.price:.2f}"

    def dehydrate_description(self, instance):
        """
        Возвращает описание объекта.
        Строка с описанием объекта. Если описание отсутствует, возвращает "Описание отсутствует".
        """
        return instance.description or "Описание отсутствует"

    def dehydrate_available(self, obj):
        """
        Возвращает строку, указывающую на наличие объекта.
        "Есть в наличии", если объект доступен, "Нет в наличии" в противном случае.
        """
        if obj.available:
            return "Есть в наличии"
        return "Нет в наличии"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Класс для управления категориями товаров в админ-панели.
    """

    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Класс для управления брендами товаров в админ-панели.
    """

    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
    Класс для управления товарами в админ-панели.
    """

    resource_class = ProductResource
    list_display = [
        "name",
        "price",
        "brand",
        "category",
        "available",
        "updated",
        "get_short_description",
    ]
    list_filter = ["available", "created", "updated", "brand", "category"]
    list_editable = ["price", "available"]
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ["name"]
    # raw_id_fields = ('category', 'brand')
    # readonly_fields = ('slug',)
    search_fields = (
        "name",
        "category__name",
        "brand__name",
        "slug",
        "price",
        "description",
        "updated",
    )
    date_hierarchy = "updated"

    def get_short_description(self, obj):
        """
        Возвращает краткое описание объекта.
        Описание объекта, сокращенное до первых пятидесяти символов.
        """
        return (
            obj.description[:50] + "..."
            if len(obj.description) > 50
            else obj.description
        )
