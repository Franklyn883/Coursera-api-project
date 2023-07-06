from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,throttle_classes
from .serializers import CartSerializer, MenuItemSerializer, OrderItemSerializer, OrderSerializer, CategorySerializer
from .models import Cart, MenuItem, Order, OrderItem, Category
from rest_framework import status
from django.shortcuts import get_object_or_404
  
from django.utils import timezone
# users authentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group

#adding pagination
from django.core.paginator import Paginator,EmptyPage

#for throttling
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
# Create your views here.


@api_view(['POST', 'GET', "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        #for filtering
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        if category_name:
            items = items.filter(category__title = category_name)#the double underscore is for lookup.
        if to_price:
            items = items.filter(price__lte = to_price)
        if search:
            items = items.filter(title__icontains = search) 
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        
        #for pagination
        perpage = request.query_params.get('perpage',default=2)
        page = request.query_params.get('page', default=1)
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data, status.HTTP_200_OK)

    elif request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
        if request.user.groups.filter(name="Manager").exists():
            serialized_items = MenuItemSerializer(data=request.data)
            serialized_items.is_valid(raise_exception=True)
            serialized_items.save()
            return Response(serialized_items.data, status.HTTP_201_CREATED)
        else:
            return Response({"Message": "Access denied"}, status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    serialized_item = MenuItemSerializer(item)

    if request.method == 'GET':
        return Response(serialized_item.data)

    if request.user.groups.filter(name="Manager").exists():
        if request.method == 'DELETE':
            item.delete()
            return Response({'Message': "Item removed successfully"}, status.HTTP_200_OK)
        elif request.method == "PUT" or request.method == "PATCH":
            data = request.data  # Use request.data to access the deserialized data

            # Update the item fields with the new data
            serializer = MenuItemSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()

            return Response({'Message': 'Item updated successfully'}, status.HTTP_200_OK)
    else:
        return Response({"Message": "Unauthorized"}, status.HTTP_403_FORBIDDEN)

# manager views for assign users to groups


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data.get('username')
    managers = Group.objects.get(name="Manager")
    if request.method == 'GET':
        managers = managers.user_set.values()  # Serialize the queryset
        return Response(managers, status=status.HTTP_200_OK)

    elif username:
        user = get_object_or_404(User, username=username)
        if request.method == 'POST':
            managers.user_set.add(user)
            return Response({'message': 'User added successfully'}, status.HTTP_200_OK)
    else:
        return Response({'message': 'error'}, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def remove_user_from_manager(request, user_id):
    user = get_object_or_404(User, id=user_id)
    managers = Group.objects.get(name="Manager")
    if request.method == 'DELETE':
        managers.user_set.remove(user)
        return Response({'message': 'User removed'}, status=status.HTTP_200_OK)

    return Response({'message': 'Unauthorized'}, status.HTTP_403_FORBIDDEN)

# Views from getting and adding delivery crew members


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def delivery_crew(request):
    username = request.data.get('username')
    delivery_crew = Group.objects.get(name="Delivery crew")
    if request.method == 'GET':
        delivery_crew = delivery_crew.user_set.values()  # Serialize the queryset
        return Response(delivery_crew, status=status.HTTP_200_OK)
    elif username:
        user = get_object_or_404(User, username=username)
        if request.method == 'POST':
            delivery_crew.user_set.add(user)
            return Response({'Message': 'User added successfully'}, status.HTTP_200_OK)

    return Response({'Message': 'Unauthorized'}, status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def remove_user_from_delivery_crew(request, user_id):
    user = get_object_or_404(User, id=user_id)
    delivery_crew = Group.objects.get(name="Delivery crew")
    if request.method == 'DELETE':
        delivery_crew.user_set.remove(user)
        return Response({'message': 'User removed'}, status=status.HTTP_200_OK)

    return Response({'message': 'Unauthorized'}, status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(request):
    if request.method == 'GET':
        items = Cart.objects.filter(user=request.user)
        serialized_items = CartSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        serialized_items = CartSerializer(
            data=request.data, context={'request': request})
        print(request.data)
        if serialized_items.is_valid(raise_exception=True):
            serialized_items.save()
            return Response(serialized_items.data, status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        items = Cart.objects.all()
        items.delete()
        return Response({'Message': 'Cart deleted'}, status.HTTP_200_OK)
    else:
        return Response({'Message:unauthorized'}, status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def order(request):
    if request.method == 'GET':
        items = Order.objects.filter(user=request.user)
        serialized_items = OrderSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
            

    elif request.method == 'DELETE':
        # Delete all orders for the user
        Order.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
