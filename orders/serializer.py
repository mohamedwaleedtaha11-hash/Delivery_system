from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Restaurant, Order, DriverLocation, Driver,
    MenuItem, OrderItem, DeliveryAssignment,
)
from . import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'user', 'phone_number', 'address']

    def validate(self, data):
        if not data.get('phone_number'):
            raise serializers.ValidationError("Phone number is required.")
        if not data.get('address'):
            raise serializers.ValidationError("Address is required.")
        return data


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'restaurant', 'name', 'description', 'is_available', 'price']


class OrderSerializer(serializers.ModelSerializer):
    total_items_count = serializers.SerializerMethodField()
    can_be_cancelled = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'order_date', 'order_id', 'status',
                  'total_items_count', 'can_be_cancelled']
        read_only_fields = ['order_id']

    def get_total_items_count(self, obj):
        return obj.get_total_items_count()

    def get_can_be_cancelled(self, obj):
        return obj.can_be_cancelled()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'item', 'quantity']


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'user', 'phone_number', 'address']

    def validate(self, data):
        if not data.get('phone_number'):
            raise serializers.ValidationError("Phone number is required.")
        if not data.get('address'):
            raise serializers.ValidationError("Address is required.")
        return data


class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLocation
        fields = ['id', 'driver', 'longitude', 'latitude']


class DeliveryAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAssignment
        fields = ['id', 'order', 'driver', 'delivery_date', 'status']