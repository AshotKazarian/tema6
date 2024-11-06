from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from .models import Category, Brand, Product
from simple_history import register

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'brand__name', 'category__name', 'available', 'description', 'created', 'updated')       

    def dehydrate_price(self, obj):
        return f"{obj.price:.2f}"
        
    def dehydrate_description(self, instance):
        return instance.description or "Описание отсутствует"
        
    def dehydrate_available(self, obj):
        if obj.available:
            return "Есть в наличии"
        else:
            return "Нет в наличии"            
        
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['name', 'slug']
  prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
  list_display = ['name', 'slug']
  prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, ExportActionMixin):
  resource_class = ProductResource
  list_display = ['name', 'price', 'brand', 'category', 'available', 'updated', 'get_short_description'] 
  list_filter = ['available', 'created', 'updated', 'brand', 'category']
  list_editable = ['price', 'available']
  prepopulated_fields = {'slug': ('name',)}
  list_display_links = ['name'] 
  # raw_id_fields = ('category', 'brand')
  # readonly_fields = ('slug',)
  search_fields = ('name', 'category__name', 'brand__name', 'slug', 'price', 'description', 'updated',) 
  date_hierarchy = 'updated'


  def get_short_description(self, obj):
    return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description


