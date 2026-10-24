from django.contrib import admin


from .models import User, Restaurant, Order, Driver, MenuItem, OrderItem

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number', 'address')
    list_filter = ()

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number')
    search_fields = ('name', 'address', 'phone_number')
    list_filter = ()

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'name', 'description', 'is_available', 'price')
    search_fields = ('restaurant__name', 'name', 'description')
    list_filter = ()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'order_date', 'order_id', 'status')
    search_fields = ('user__user__username', 'restaurant__name', 'status')
    list_filter = ()

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity')
    search_fields = ('item__name',)
    list_filter = ()

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__user__username', 'phone_number', 'address')
    list_filter = ()