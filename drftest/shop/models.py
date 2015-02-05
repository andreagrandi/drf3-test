from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    # Setting this field to True means that this Product will let customer to collect Stamps
    collect_stamp = models.BooleanField(default=False)


class Stamp(models.Model):
    user = models.ForeignKey(User)
    redeemed = models.BooleanField(default=False)


class Order(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.BigIntegerField()


class Voucher(models.Model):
    user = models.ForeignKey(User)
    redeemed = models.BooleanField(default=False)
