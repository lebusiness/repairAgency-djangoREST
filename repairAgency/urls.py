"""repairAgency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers
from app.views import *

router = routers.DefaultRouter()
# позволяет прослушивать 'root' и его get_queryset(/<id/int>)
router.register(r'categories', CategoriesAPIView, basename='categories')
router.register(r'feedbacks', FeedbackAPIView, basename='feedbacks')
router.register(r'services', ServiceAPIView, basename='services')
router.register(r'cart', CartAPIView, basename='cart')
router.register(r'cart-order', RelationCartServiceView, basename='cart-order')
# маршрутизация
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('djoser.urls')),  
    re_path(r'^auth/', include('djoser.urls.authtoken')), 
]