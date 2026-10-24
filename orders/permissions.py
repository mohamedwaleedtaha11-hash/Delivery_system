from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

def _is_authenticated(request):
    return request.user and request.user.is_authenticated()

class UserIsOwner(permissions.BasePermission):
    """ اليوزر لازم يكون ادمن """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class RestaurantIsOwner(permissions.BasePermission):
    """ اليوزر لازم يكون ادمن """
    def has_object_permission(self, request, view, obj):
        return obj.restaurant.user == request.user

class OrderPermission(permissions.BasePermission):
    """ السماح بالوصول فقط العميل صاحب الاوردر او  المطعم """
    def has_object_permission(self, request, view, obj):
        is_costumer = request.user == obj.user
        is_restaurant = request.user == obj.restaurant.user
        return is_costumer or is_restaurant

class OrderItemPermission(permissions.BasePermission):
    """ السماح بالوصول فقط العميل صاحب الاوردر """
    def has_object_permission(self, request, view, obj):
        is_costumer = request.user == obj.order.user
        is_restaurant = request.user == obj.order.restaurant.user
        return is_costumer or is_restaurant

class DriverPermission(permissions.BasePermission):     
    """ السماح بالوصول فقط العميل صاحب الاوردر """
    def has_object_permission(self, request, view, obj):
        is_driver = request.user == obj.order.driver
        is_costumer = request.user == obj.order.user
        return is_driver or is_costumer
class DriverLocationPermission(permissions.BasePermission):     
    """ السماح بالوصول فقط العميل صاحب الاوردر """
    def has_object_permission(self, request, view, obj):
        is_driver = request.user == obj.driver
        is_costumer = request.user == obj.driver.user
        return is_driver or is_costumer

class DeliveryAssignmentPermission(permissions.BasePermission):     
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            is_driver = request.user == obj.driver.user
            is_costumer = request.user == obj.order.user
            return is_driver or is_costumer
        return is_driver 
OrderPermission=OrderItemPermission
DriverPermission=DriverLocationPermission