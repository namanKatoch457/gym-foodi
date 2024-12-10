"""
URL configuration for gymfinity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from foodi import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('foodi/', include('foodi.urls')),
    path('foodi/veg/', views.meal_category, {'meal_type': 'veg'}, name='veg_meal'),
    path('foodi/nonveg/', views.meal_category, {'meal_type': 'nonveg'}, name='nonveg_meal'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:food_id>',views.remove_from_cart,name='remove_from_cart'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#noni
#uziak47uzi
