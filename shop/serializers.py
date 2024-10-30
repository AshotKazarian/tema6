from rest_framework import serializers
from .models import Product, Category, Brand
import re

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = '__all__'
   
  def validate_price(self, value):
      if value <0:
          raise serializers.ValidationError("Цена не может быть меньше нуля.")
      
      return value 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
    def validate(self, data):
        name = data.get('name')
        if not re.match(r'^[а-яА-Я\s]+$', name):
            raise serializers.ValidationError("Название категории может быть написано только на кириллице.")
            
        return data
    
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
    
    def validate(self, data):
        name = data.get('name')
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise serializers.ValidationError("Название бренда может быть написано только на латинице.")
            
        return data