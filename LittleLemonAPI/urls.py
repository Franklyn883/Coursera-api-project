from django.urls import path,include
from . import views


urlpatterns = [
  path('menu-items',views.menu_items),
  path('menu-items/<int:pk>',views.menu_item),
  path('login/', include('djoser.urls')),
  path('users/', include('djoser.urls'))
 
]