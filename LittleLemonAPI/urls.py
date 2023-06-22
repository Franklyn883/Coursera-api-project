from django.urls import path,include
from . import views



urlpatterns = [
  path('menu-items',views.menu_items),
  path('menu-items/<int:pk>',views.menu_item),
  path('auth/users/',views.CustomRegistrationView.as_view({'post':'create'})),

 
]