from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('restaurants', views.RestaurantViewSet, basename='restaurant')
router.register('orders', views.OrderViewSet, basename='order')
router.register('drivers', views.DriverViewSet, basename='driver')
router.register('menu_items', views.MenuItemViewSet, basename='menu_item')
router.register('driver_locations', views.DriverLocationViewSet, basename='driver_location')
router.register('delivery_assignments', views.DeliveryAssignmentViewSet, basename='delivery_assignment')
urlpatterns = router.urls