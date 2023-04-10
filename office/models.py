from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.html import escape, mark_safe

# Create your models here.
class User(AbstractBaseUser):
    REQUIRED_FIELDS = ('id', 'name', 'email', 'password')
    USERNAME_FIELD = ('username')

    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, null=True)

class Deliveries(models.Model):
    deliveryperson = models.ForeignKey(User, on_delete=models.CASCADE)
    deliveries = models.IntegerField()

class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class DeliveryList(models.Model):
    id = models.IntegerField(primary_key=True)
    deliveryperson = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class ProductList(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    date_published = models.DateField()