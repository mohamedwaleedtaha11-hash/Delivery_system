from django.contrib import admin


from .models import User, Restaurant, Order, Driver, MenuItem, OrderItem

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user', 'phone_number', 'address')
    list_filter = ()

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number')
    search_fields = ('name', 'address', 'phone_number')
    list_filter = ()

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'name', 'description', 'is_available', 'price')
    search_fields = ('restaurant__name', 'name', 'description', 'is_available', 'price')
    list_filter = ()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'order_date', 'order_id', 'status')
    search_fields = ('user', 'restaurant', 'order_date', 'order_id', 'status')
    list_filter = ()

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity')
    search_fields = ('order', 'item', 'quantity')
    list_filter = ()

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user', 'phone_number', 'address')
    list_filter = ()