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
    
    def validate_price(self,value):
      if(value < 0):
        raise serializers.ValidationError('price should be more that zero')
    
    
class CartSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cart
    fields = ['id','quantity','unit_price', 'price']
    depth = 1
    
    def validate(self,attrs):
      if(attrs['quantity']<0):
        raise serializers.ValidationError("Quantity should be more than 0")
      if(attrs['unit_price']<0):
        raise serializers.ValidationError("price should be more than zero")
      return super().validate(attrs)
    
class OrderSerializer(serializers.ModelSerializer):
  
  model = Order
  fields = ['id', 'status','total','date']
  depth = 1
  
class OrderItemSerializer(serializers.ModelSerializer):
  unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
  quantity = serializers.IntegerField()
  model = OrderItem
  fields = ['id', 'quantity', 'unit_price','price']
  depth = 1
  
  