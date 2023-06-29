from rest_framework import serializers 
from .models import Category,MenuItem,Cart,Order,OrderItem
from rest_framework.validators import UniqueTogetherValidator
import bleach

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id','slug','title']
    
class MenuItemSerializer(serializers.ModelSerializer):

  category = CategorySerializer(read_only=True)
  # To bring even more detailed result from the Category model
 # category = CategorySerializer()
  category_id = serializers.IntegerField(write_only=True)
  
  class Meta:
    model = MenuItem
    fields = ['id','title','price', 'featured','category','category_id']
    
    def validate_price(self,value):
      if(value < 0):
        raise serializers.ValidationError('price should be more that zero')
      
    #to clean the data
    def validate(self,attrs):
      attrs['title'] = bleach.clean(attrs['title'])
      
      return super().validate(attrs)
    
    
class CartSerializer(serializers.ModelSerializer):

  user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
  class Meta:
    model = Cart
    fields = ['id','user','menuitem','quantity','unit_price', 'price','menuitem']
    validators = [
       UniqueTogetherValidator(
       queryset=Cart.objects.all(),
       fields=['user','menuitem']
    ),
  ]
  def create(self, validated_data):
    cart = Cart.objects.create(
    user=self.context['request'].user,
    **validated_data
        )
    return cart
  def validate(self,attrs):
      if attrs['quantity']<0:
        raise serializers.ValidationError("Quantity should be more than 0")
      if attrs['unit_price']<0:
        raise serializers.ValidationError("price should be more than zero")
      return attrs
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
  validators = [
       UniqueTogetherValidator(
       queryset=OrderItem.objects.all(),
       fields=['menuitem','order']
    ),
  ]
  