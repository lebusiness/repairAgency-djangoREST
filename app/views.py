from rest_framework import generics
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import mixins
from .models import *
from .serializers import *
import logging
import json
from django.core import serializers
# представления


class CategoriesAPIView(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    # класс, отвечающий за кол-во ключей и за конверт в JSON
    serializer_class = CategoriesSerializer
    lookup_field = "slug"
    queryset = Category.objects.all()

    # setter queryset
    # def get_queryset(self):
    #   # pk = /caregories/<id>

    #   # vannaya - slug
    #   pk = self.kwargs.get("pk")
    #   queryset = self
    #   logger = logging.getLogger("mylogger")
    #   logger.info(queryset)
    #   # вывести первые 4
    #   if not pk:
    #     return Category.objects.all()[:4]

    #   # вывести только конкретный
    #   return Category.objects.filter(pk=pk)

    # добавляет путь categories/category (тут реализуем вывод только названий категорий)
    @action(methods=['get'], detail=False)
    def short(self, request):
        cats = Category.objects.all()
        return Response({'cats': [{'id': c.id, 'name': c.name, 'slug': c.slug, 'descr': c.descr, 'img': 'media/'+str(c.img)} for c in cats]})


class FeedbackAPIView(mixins.CreateModelMixin,
                      GenericViewSet):
    # класс, отвечающий за кол-во ключей и за конверт в JSON
    serializer_class = FeedbacksSerializer
    queryset = Category.objects.all()


class ServiceAPIView(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    # класс, отвечающий за кол-во ключей и за конверт в JSON
    serializer_class = ServicesSerializer
    lookup_field = "slug"
    queryset = Service.objects.all()


class CartAPIView(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    # вывод list заказов корзины
    def retrieve(self, request, *args, **kwargs):
        logger = logging.getLogger("mylogger")
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # выцепить id услуги и id связи в массив
        serviceIdArr = []
        relationIdArr = []
        for i in serializer.data['rel_services']:
            serviceIdArr.append(i['service'])
            relationIdArr.append(i['id'])


        servicesORM = Service.objects.all().filter(pk__in=serviceIdArr)
        services = ServicesSerializer(servicesORM, many=True)

        index = 0
        for i in services.data:
            i.update({'relationId': relationIdArr[index]})
            index += 1
        return Response(services.data)


class RelationCartServiceView(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              GenericViewSet):

    serializer_class = RelationCartServiceSerializer
    queryset = RelationCartService.objects.all()
