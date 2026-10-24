from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}"

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    def __str__(self):
        return f"{self.name}"
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    price = models.FloatField()
    def __str__(self):
        return f"{self.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    status = models.CharField(
        max_length=10,
        choices=(
            ('pending', 'pending'),
            ('delivered', 'delivered'),
            ('cancelled', 'cancelled'),
            ('completed', 'completed'),
            ('failed', 'failed'),
            ('accepted', 'accepted'),
            ('rejected', 'rejected'),
        )
    )
    def __str__(self):
            return f"Order #{self.id}"

    def get_total_items_count(self):
        return sum(item.quantity for item in self.items.all())

    def can_be_cancelled(self):
        return self.status == 'pending'

class OrderItem(models.Model):
     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
     item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
     quantity = models.IntegerField()
     def __str__(self):
         return f"{self.order.id}"

class Driver(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
     phone_number = models.CharField(max_length=15, blank=True, null=True)
     address = models.TextField(blank=True, null=True)
     def __str__(self):
         return f"{self.user}"

class DriverLocation(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    def __str__(self):
        return f"{self.driver.user.username}"

class DeliveryAssignment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    delivery_date = models.DateTimeField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'pending'),
            ('delivered', 'delivered'),
            ('cancelled', 'cancelled'),
            ('completed', 'completed'),
            ('failed', 'failed'),
            ('accepted', 'accepted'),
            ('rejected', 'rejected'),
        )
    )

    def can_be_accepted(self):
        return self.status == 'pending'

    def can_be_rejected(self):
        return self.status == 'pending'

    def accept(self):
        if not self.can_be_accepted():
            raise ValidationError("This delivery assignment cannot be accepted.")
        self.status = 'accepted'
        self.save()
    def reject(self):
        if not self.can_be_rejected():
            raise ValidationError("This delivery assignment cannot be rejected.")
        self.status = 'rejected'
        self.save()
    
    def __str__(self):
        return f"{self.order.id}"