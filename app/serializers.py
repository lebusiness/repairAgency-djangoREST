from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class ServicesSerializer(serializers.ModelSerializer):

  class Meta:
    model = Service
    fields = ('id', 'name', 'price', 'summary', 'descr', 'img', 'slug')

class RelationCartServiceSerializer(serializers.ModelSerializer):

  class Meta:
    model = RelationCartService
    fields = ('id','cart','service')

class FeedbacksSerializer(serializers.ModelSerializer):

  class Meta:
    model = Feedback
    fields = ('name', 'text', 'category', 'valuation', 'id')

class CategoriesSerializer(serializers.ModelSerializer):
  # из таблицы Category возращает поля field
  services = ServicesSerializer(many=True, read_only=True)
  feedbacks = FeedbacksSerializer(many=True, read_only=True)
  class Meta:
    model = Category
    fields = ('id', 'name', 'descr', 'slug', 'img', 'services', 'feedbacks')
    # extra_kwargs = {
    #   'id': {'source': 'name', 'read_only': True}
    # }

class CartSerializer(serializers.ModelSerializer):
  rel_services = RelationCartServiceSerializer(many=True, read_only=True)
  class Meta:
    model = Cart
    fields = ('id', 'user', 'rel_services')

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ('id', 'name')

class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = ('services', 'number', 'price', 'user', 'address')