from rest_framework import serializers 
from .models import Category,MenuItem,Cart,Order,OrderItem

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id','slug','title']
    
class MenuItemSerializer(serializers.ModelSerializer):
  Category = CategorySerializer()
  
  class Meta:
    model = MenuItem
    fields = ['id','title','price', 'featured','category']
    
    
    
class CartSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cart
    fields = ['id','quantity','unit_price', 'price']
    depth = 1
    
class OrderSerializer(serializers.ModelSerializer):
  model = Order
  fields = ['id', 'status','total','date']
  depth = 1
  
class OrderItemSerializer(serializers.ModelSerializer):
  model = OrderItem
  fields = ['id', 'quantity', 'unit_price','price']
  depth = 1