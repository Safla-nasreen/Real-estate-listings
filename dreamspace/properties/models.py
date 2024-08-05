from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    city = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city},{self.State},{self.country}"


class PropertyType(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='properties')

    def __str__(self):
        return self.name


class Property(models.Model):
    title = models.CharField(max_length=200)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    description = models.TextField()
    address = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties')
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.title} in cart of {self.cart.user.username}"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id
