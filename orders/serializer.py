from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Restaurant, Order, DriverLocation, Driver, MenuItem, OrderItem, DeliveryAssignment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'address']

    def validate(self, data):
        if not data.get('phone_number'):
            raise serializers.ValidationError("Phone number is required.")
        if not data.get('address'):
            raise serializers.ValidationError("Address is required.")
        return data
    class Meta:
        model = User
        fields = ['user', 'phone_number', 'address']

class RestaurantSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError("Name is required.")
        if not data.get('address'):
            raise serializers.ValidationError("Address is required.")
        if not data.get('phone_number'):
            raise serializers.ValidationError("Phone number is required.")
        return data
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone_number']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'is_available', 'price']

class MenuItemSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError("Name is required.")
        if not data.get('price'):
            raise serializers.ValidationError("Price is required.")
        return data
    class Meta:
        model = Restaurant
        fields = ['name', 'price']

class OrderSerializer(serializers.ModelSerializer):
    total_items_count = serializers.SerializerMethodField()
    can_be_cancelled = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'order_date', 'order_id', 'status',
                'total_items_count', 'can_be_cancelled']
        read_only_fields = ['order_id']
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'item', 'quantity']
    
class DriverSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError("Name is required.")
        if not data.get('phone_number'):
            raise serializers.ValidationError("Phone number is required.")
        if not data.get('address'):
            raise serializers.ValidationError("Address is required.")
        return data
    class Meta:
        model = Driver
        fields = ['name', 'phone_number', 'address']

class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLocation
        fields = ['driver', 'longitude', 'latitude']

class DeliveryAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAssignment
        fields = ['order', 'driver', 'delivery_date']
        read_only_fields = ['order']