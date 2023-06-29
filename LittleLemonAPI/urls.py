from django.urls import path,include
from . import views



urlpatterns = [
  path('menu-items',views.menu_items),
  path('menu-items/<int:pk>',views.menu_item),
  path('groups/manager/users', views.managers),
  path('groups/manager/users/<int:user_id>',views.remove_user_from_manager),
  path('groups/delivery-crew/users', views.delivery_crew),
  path('groups/delivery-crew/users/<int:user_id>',views.remove_user_from_delivery_crew),
  path('cart/menu-items',views.cart),


 
]