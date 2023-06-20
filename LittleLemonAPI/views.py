from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CartSerializer,MenuItemSerializer,OrderItemSerializer,OrderSerializer,CategorySerializer
from .models import Cart,MenuItem,Order,OrderItem,Category
# Create your views here.
@api_view()
def menu_items(request):
  items = MenuItem.objects.select_related('category').all()
  serialized_items = MenuItemSerializer(items, many=True)
  return Response(serialized_items.data)
