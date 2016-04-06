from django.db import models


class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    sex = models.CharField(max_length=6)
    birthday = models.DateField()
    address = models.CharField(max_length=255)
    auth_time = models.DateTimeField()
    request_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.IntegerField()
    is_active = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem', through_fields=('order_id', 'item_id'))
    user = models.ForeignKey(User)
    state = models.CharField(max_length=10)
    fixed_amount = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    item = models.ForeignKey(Item)
    count_item = models.IntegerField()
