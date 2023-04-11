from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.html import escape, mark_safe
from django.contrib.auth.models import UserManager

# Create your models here.
class User(AbstractBaseUser):
    REQUIRED_FIELDS = ('id', 'name', 'password')
    USERNAME_FIELD = ('username')

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    user_type = models.IntegerField(choices=((0,0), (1,1)), default=0)
    deliveries = models.IntegerField(default=0)
    salary = models.FloatField(default=0)

    objects = UserManager()

    def __str__(self):
        return self.username

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    due_days = models.IntegerField(default=0)
    pause = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class ProductList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, null=True)
    price = models.IntegerField(default=0)
    date_published = models.DateField()

    def __str__(self):
        return self.code

class SubscriptionList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'product'], name='unique_customer_product_subscription'
            )
        ]

class DeliveryList(models.Model):
    deliveryperson = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['deliveryperson', 'customer'], name='unique_deliveryperson_customer_deliverylist'
            )
        ]

class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'product'], name='unique_customer_product_bill'
            )
        ]

# class CustomerRequest(models.Model):
