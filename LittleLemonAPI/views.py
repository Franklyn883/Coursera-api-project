from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CartSerializer,MenuItemSerializer,OrderItemSerializer,OrderSerializer,CategorySerializer
from .models import Cart,MenuItem,Order,OrderItem,Category
from rest_framework import status
from django.shortcuts import get_object_or_404
# Create your views here.
@api_view(['POST','GET'])
def menu_items(request):
  if request.method == 'GET':
    items = MenuItem.objects.select_related('category').all()
    serialized_items = MenuItemSerializer(items, many=True)
    return Response(serialized_items.data, status.HTTP_200_OK)
  
  elif request.method == 'POST':
    serialized_items = MenuItemSerializer(data = request.data)
    serialized_items.is_valid(raise_exception=True)
    serialized_items.save()
    return Response(serialized_items.data,status.HTTP_201_CREATED)
  
  
@api_view(['GET','POST','PATCH','PUT','DELETE'])
def menu_item(request, pk):
 
  item = get_object_or_404(MenuItem, pk=pk)
  #here notice we didn't ass the many=True argument because it's not a list.
  serialized_item = MenuItemSerializer(item)
  return Response(serialized_item.data)