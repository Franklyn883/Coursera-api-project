from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CartSerializer,MenuItemSerializer,OrderItemSerializer,OrderSerializer,CategorySerializer
from .models import Cart,MenuItem,Order,OrderItem,Category
from rest_framework import status
# Create your views here.
@api_view(['POST','GET'])
def menu_items(request):
  if request.method == 'GET':
    items = MenuItem.objects.select_related('category').all()
    serialized_items = MenuItemSerializer(items, many=True)
    return Response(serialized_items.data)
  
  elif request.method == 'POST':
    serialized_items = MenuItemSerializer(data = request.data)
    serialized_items.is_valid(raise_exception=True)
    serialized_items.save()
    return Response(serialized_items.data,status.HTTP_201_CREATED)