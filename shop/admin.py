"""
Этот модуль реализует админ-панель для django проекта.
"""

from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from django.utils import timezone
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from .models import Category, Brand, Product, Comment


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

class CommentInline(admin.StackedInline):
    model = Comment

@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """
    Класс для управления товарами в админ-панели.
    """

    resource_class = ProductResource
    list_display = [
        "name",
        "price",
        "brand",
        "category",
        "image_visible",
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
    
    inlines = [
        CommentInline,
    ]

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
    def image_visible(self, obj):
        """
        Позволяет просматривать изображение товара непосредственно в панели администратора
        """
        if obj.image:
            return mark_safe("<img src='{}' width='80' />".format(obj.image.url))
        return "Нет изображения"
    image_visible.__name__ = "Изображение"
    
    def make_unavailable(self, request, queryset):
        """
        Действие для установки доступности товара в "Нет в наличии".
        """
        updated_count = queryset.update(available=False)
        self.message_user(request, f"{updated_count} товара(ов) отмечены как 'Нет в наличии'.")

    def make_available(self, request, queryset):
         """
         Действие для установки доступности товара в "Есть в наличии".
         """
         updated_count = queryset.update(available=True)
         self.message_user(request, f"{updated_count} товара(ов) отмечены как 'Есть в наличии'.")
    
    def generate_pdf(self, request, queryset):
        """
        Действие для генерации PDF-документа с информацией о выбранных товарах.
        """
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        y_position = 10.5 * inch  # Начальная позиция по оси Y

        for product in queryset:
            textobject = p.beginText()
            textobject.setTextOrigin(inch, y_position)  # Устанавливаем позицию текста
            textobject.setFont("Helvetica", 12)
            textobject.textLine(f"Name: {product.name}")
            textobject.textLine(f"Price, RUB: {product.price}")
            textobject.textLine(f"Brand: {product.brand.name}")
            textobject.textLine(f"Category: {product.category.slug}")
            textobject.textLine(f"Available: {'Yes' if product.available else 'No'}")
            textobject.textLine("-" * 30)

            p.drawText(textobject)
            y_position -= 1.5 * inch  # Корректируем позицию для следующей записи
            
            if y_position <= inch:  # Проверяем не ушли ли мы вниз страницы
                p.showPage()  # Начинаем новую страницу
                y_position = 10.5 * inch  # Возвращаем позицию к началу новой страницы

        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='products.pdf')
    
    make_unavailable.short_description = "Отметить как 'Нет в наличии'"
    make_available.short_description = "Отметить как 'Есть в наличии'"
    generate_pdf.short_description = "Сгенерировать PDF"    
    actions = ['make_unavailable', 'make_available', 'generate_pdf']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'body', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'body']
    