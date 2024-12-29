from django import template
from ..models import Product, Category, Brand

register = template.Library()

@register.simple_tag
def total_products():
    return Product.objects.all().count() 

@register.simple_tag(takes_context=True)
def total_products_by_category(context):
    category = context['category']
    return Category.objects.all().exclude(name__icontains='test').count()

@register.simple_tag(takes_context=True)
def total_products_by_brand(context):
    brand = context['brand']
    return Brand.objects.all().exclude(name__icontains='test').count()