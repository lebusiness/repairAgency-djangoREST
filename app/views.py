from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework import generics
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework import mixins
from .models import *
from .serializers import *
import logging
from django.core import serializers
from django.db.models import Q


class PaginagitonDefault(PageNumberPagination):
    page_size = 100

    def get_paginated_response(self, data):
        return Response(data)

class PaginagitonCategories(PageNumberPagination):
    page_size = 4

    def get_paginated_response(self, data):
        return Response({
            'result': data,
            'count': self.page.paginator.count
        })

class CategoriesAPIView(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    # класс, отвечающий за кол-во ключей и за конверт в JSON
    serializer_class = CategoriesSerializer
    lookup_field = "slug"
    queryset = Category.objects.all()
    pagination_class = PaginagitonCategories
    # только категории

    @action(methods=['get'], detail=False)
    def short(self, request):
        cats = Category.objects.all()
        url = request.build_absolute_uri('/')
        return Response([{'id': c.id, 'name': c.name, 'slug': c.slug, 'descr': c.descr, 'img': url + 'media/'+str(c.img)} for c in cats])

    @action(methods=['get'], detail=False)
    def search(self, request):
        query = self.request.GET.get('q')
        object_list = Category.objects.filter(
            Q(name__icontains=query) | Q(
                descr__icontains=query) | Q(slug__icontains=query)
        )
        return Response(CategoriesSerializer(object_list, many=True).data)


class FeedbackAPIView(mixins.CreateModelMixin,
                      GenericViewSet):
    # класс, отвечающий за кол-во ключей и за конверт в JSON
    serializer_class = FeedbacksSerializer
    queryset = Category.objects.all()
    pagination_class = PaginagitonDefault


class ServiceAPIView(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    # класс, отвечающий за кол-во ключей и за конверт в JSON
    serializer_class = ServicesSerializer
    lookup_field = "slug"
    queryset = Service.objects.all()
    pagination_class = PaginagitonDefault

class CartAPIView(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    pagination_class = PaginagitonDefault

    # вывод list заказов корзины
    def retrieve(self, request, *args, **kwargs):
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
        url = request.build_absolute_uri('/')
        index = 0
        for i in services.data:
            i['img'] = url + i['img']
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
    pagination_class = PaginagitonDefault

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data)


class OrderView(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    pagination_class = PaginagitonDefault

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # если уже есть такое заказ, не добавлять
        ordersSet = Order.objects.all()
        user = serializer.validated_data['user']
        userOrders = ordersSet.filter(user=user)
        serUserOrders = userOrders
        if serUserOrders.count() != 0:
            return Response(status=status.HTTP_409_CONFLICT)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
