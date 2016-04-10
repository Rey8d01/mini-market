"""Сериализаторы для API."""
from rest_framework import serializers
from .models import Item, Order, User


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'title', 'description', 'amount')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'sex', 'address')


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    items = ItemSerializer(many=True)  # Связь для М-М

    class Meta:
        model = Order
        fields = ('id', 'state', 'fixed_amount', 'user', 'items')
