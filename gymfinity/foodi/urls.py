from django.contrib import admin
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('foodi/veg/', views.meal_category, {'meal_type': 'veg'}, name='veg_meal'),
    path('foodi/nonveg/', views.meal_category, {'meal_type': 'nonveg'}, name='nonveg_meal'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('register/', views.register, name='register'),
    path('checkout',views.checkout,name='checkout'),
    path('place_order',views.place_order,name='place_order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)