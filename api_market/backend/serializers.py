from rest_framework import serializers
from .models import Item, Order, User


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    items = serializers.HyperlinkedIdentityField('items')

    class Meta:
        model = Order
