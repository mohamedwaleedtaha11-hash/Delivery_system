from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models
from .models import (
    Restaurant, MenuItem, Order, OrderItem,
    Driver, DriverLocation, DeliveryAssignment,
)
from .permissions import (
    UserIsOwner, RestaurantIsOwner, OrderPermission, DriverPermission,
)
from .serializer import (
    ProfileSerializer, RestaurantSerializer, OrderSerializer,
    DriverSerializer, DriverLocationSerializer, MenuItemSerializer,
    OrderItemSerializer, DeliveryAssignmentSerializer,
)

Profile = models.User  


class UserViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, UserIsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'phone_number', 'address']


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, RestaurantIsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'address', 'phone_number']


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'description', 'is_available', 'price']

    @action(detail=True, methods=['post'])
    def order(self, request, pk=None):
        menu_item = self.get_object()
        if not menu_item.is_available:
            return Response({'message': 'This item is not available.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({'message': 'Create a profile first.'},
                            status=status.HTTP_400_BAD_REQUEST)
        quantity = int(request.data.get('quantity', 1))
        order = Order.objects.create(
            user=profile, restaurant=menu_item.restaurant, status='pending'
        )
        OrderItem.objects.create(order=order, item=menu_item, quantity=quantity)
        return Response({'message': 'Order placed successfully.', 'order_id': order.id},
                        status=status.HTTP_201_CREATED)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, OrderPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'restaurant', 'order_date', 'order_id', 'status']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.user.user != request.user:
            raise PermissionDenied("You do not have permission to cancel this order.")
        if not order.can_be_cancelled():
            return Response({'message': 'This order cannot be cancelled.'},
                            status=status.HTTP_400_BAD_REQUEST)
        order.status = 'cancelled'
        order.save()
        return Response({'message': 'Order cancelled successfully.'},
                        status=status.HTTP_200_OK)


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'item', 'quantity']


class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, DriverPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'phone_number', 'address']


class DriverLocationViewSet(ModelViewSet):
    queryset = DriverLocation.objects.all()
    serializer_class = DriverLocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['driver', 'longitude', 'latitude']


class DeliveryAssignmentViewSet(ModelViewSet):
    queryset = DeliveryAssignment.objects.all()
    serializer_class = DeliveryAssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'driver', 'delivery_date']