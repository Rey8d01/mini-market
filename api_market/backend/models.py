from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    sex = models.CharField(max_length=6, blank=True)
    birthday = models.DateField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    auth_time = models.DateTimeField(auto_now_add=True)
    request_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.IntegerField()
    is_active = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem', through_fields=('order_id', 'item_id'))
    user = models.ForeignKey(User)
    state = models.IntegerField(default=1)
    fixed_amount = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    STATE_CART = 1
    STATE_CONFIRMED = 2
    STATE_SHIPPING = 3
    STATE_CANCEL = 4
    STATE_COMPLETE = 5


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    item = models.ForeignKey(Item)
    count_item = models.IntegerField()
