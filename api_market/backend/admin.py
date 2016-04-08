from django.contrib import admin

from .models import Order, Item, User

admin.site.register(Order)
admin.site.register(Item)
admin.site.register(User)
