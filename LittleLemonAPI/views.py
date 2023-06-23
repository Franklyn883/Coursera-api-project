from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import CartSerializer,MenuItemSerializer,OrderItemSerializer,OrderSerializer,CategorySerializer
from .models import Cart,MenuItem,Order,OrderItem,Category
from rest_framework import status
from django.shortcuts import get_object_or_404

#users authentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.contrib.auth.models import User,Group

# Create your views here.


  

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
    
#manager views for assign users to groups

@permission_classes([IsAdminUser])
@api_view(['GET','POST','DELETE'])
def managers(request):
  username = request.data.get('username')
  
  if username:
    user = get_object_or_404(User,username=username)
    managers=Group.objects.get(name="Manager")
    if request.method == 'GET':
      serialized_managers = list(managers.user_set.values())  # Serialize the queryset
      return Response(serialized_managers, status=status.HTTP_200_OK)
    elif request.method == 'POST':
      managers.user_set.add(user)
      return Response({'message':'User added successfully'}, status.HTTP_200_OK)
    elif request.method == 'DELETE':
      managers.user_set.remove(user)
      return Response({'Message':'user removed'},status.HTTP_200_OK)
  return Response({'message':'error'},status.HTTP_400_BAD_REQUEST)
  