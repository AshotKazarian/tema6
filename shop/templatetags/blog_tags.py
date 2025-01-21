from django import template
from ..models import Product, Category, Brand

register = template.Library()

@register.simple_tag
def total_products():
    return Product.objects.count() 

@register.simple_tag(takes_context=True)
def total_products_by_category(context):
    category = context['category']
    return Category.objects.exclude(name__icontains='test').count()

@register.simple_tag(takes_context=True)
def total_products_by_brand(context):
    brand = context['brand']
    return Brand.objects.exclude(name__icontains='test').count()
    
@register.inclusion_tag('shop/includes/new_products.html')
def new_products():
    products = Product.objects.order_by('-created')[:3]
    return {'new_products': products}