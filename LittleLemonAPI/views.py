from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import CartSerializer,MenuItemSerializer,OrderItemSerializer,OrderSerializer,CategorySerializer
from .models import Cart,MenuItem,Order,OrderItem,Category
from rest_framework import status
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
#users authentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

#userscreation

class CustomRegistrationView(UserViewSet):
    # Customize registration behavior if needed
    pass
  
  

@api_view(['POST','GET',"PUT","DELETE"])
@permission_classes([IsAuthenticated])
def menu_items(request):
  if request.method == 'GET':
    items = MenuItem.objects.select_related('category').all()
    serialized_items = MenuItemSerializer(items, many=True)
    return Response(serialized_items.data, status.HTTP_200_OK)
  
  elif request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
    if request.user.groups.filter(name="Manager").exists():
      serialized_items = MenuItemSerializer(data = request.data)
      serialized_items.is_valid(raise_exception=True)
      serialized_items.save()
      return Response(serialized_items.data,status.HTTP_201_CREATED)
    else:
      return Response({"Message":"Access denied"} ,status.HTTP_403_FORBIDDEN)
    
  
@api_view(['GET','POST','PATCH','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def menu_item(request, pk):
  item = get_object_or_404(MenuItem, pk=pk)
  serialized_item = MenuItemSerializer(item)
  
  if request.method == 'GET':
    return Response(serialized_item.data)
  
  elif request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
    if request.user.groups.filter(name="Manager").exists():
      return Response(serialized_item.data, status.HTTP_200_OK)
    else:
      return Response({"Message":"Unauthorized"} ,status.HTTP_403_FORBIDDEN)

