from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class UserIsOwner(permissions.BasePermission):
    """صاحب البروفايل فقط للتعديل، والقراءة للكل"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class RestaurantIsOwner(permissions.BasePermission):
    """الـ Restaurant مفيهوش مالك، فالتعديل للأدمن فقط والقراءة للكل"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class OrderPermission(permissions.BasePermission):
    """العميل صاحب الأوردر أو الأدمن"""
    def has_object_permission(self, request, view, obj):
        return obj.user.user == request.user or request.user.is_staff


class OrderItemPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.order.user.user == request.user or request.user.is_staff


class DriverPermission(permissions.BasePermission):
    """السواق نفسه أو الأدمن للتعديل، والقراءة للكل"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user.user == request.user or request.user.is_staff


class DriverLocationPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.driver.user.user == request.user or request.user.is_staff


class DeliveryAssignmentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_driver = obj.driver.user.user == request.user
        is_customer = obj.order.user.user == request.user
        if request.method in SAFE_METHODS:
            return is_driver or is_customer or request.user.is_staff
        return is_driver or request.user.is_staff