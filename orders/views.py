from urllib import request

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import ( 
User, Restaurant, Order, Driver, DeliveryAssignment
)
from .permissions import (
UserIsOwner, RestaurantIsOwner, OrderPermission, DriverPermission
)

from .serializer import (
UserSerializer, RestaurantSerializer, OrderSerializer, DriverSerializer, DriverLocationSerializer
, MenuItemSerializer, OrderItemSerializer, DeliveryAssignmentSerializer
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, UserIsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'phone_number', 'address']


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.filter()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, RestaurantIsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'address', 'phone_number']

class MenuItemViewSet(ModelViewSet):
    queryset = Restaurant.objects.filter()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'description', 'is_available', 'price']

    @action(detail=True, methods=['post'])
    def order(self, request, pk=None):
        restaurant = self.get_object()
        if restaurant.user == request.user:
            return Response({'message': 'You can not order your own restaurant.'})
        status = status.HTTPS_400_BAD_REQUEST
        return Response({
            'massage':'Order place successfully.'
        }),
        status=status.HTTPS_200_OK

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.filter()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, OrderPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'restaurant', 'order_date', 'order_id', 'status']
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.user != request.user:
            raise PermissionDenied("You do not have permission to cancel this order.")
        if not order.can_be_cancelled():
            return Response({'message': 'This order cannot be cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = 'cancelled'
        order.save()
        return Response({'message': 'Order cancelled successfully.'}, status=status.HTTP_200_OK)
class OrderItemViewSet(ModelViewSet):
    queryset = Order.objects.filter()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'item', 'quantity']

class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.filter()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, DriverPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'phone_number', 'address', 'longitude', 'latitude']

class DriverLocationViewSet(ModelViewSet):
    queryset = Driver.objects.filter()
    serializer_class = DriverLocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['driver', 'longitude', 'latitude']

class DeliveryAssignmentViewSet(ModelViewSet):
    queryset = DeliveryAssignment.objects.filter()
    serializer_class = DeliveryAssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'driver', 'delivery_date']