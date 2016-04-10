"""Сериализаторы для API."""
from rest_framework import serializers
from .models import Item, Order, User, OrderItem


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'title', 'description', 'amount')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'sex', 'address')


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='item.id')
    title = serializers.ReadOnlyField(source='item.title')
    amount = serializers.ReadOnlyField(source='item.amount')

    class Meta:
        model = OrderItem
        fields = ('id', 'title', 'amount', 'count_item')


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    # items = ItemSerializer(many=True)  # Связь для М-М
    items = OrderItemSerializer(source='orderitem_set', many=True)  # Связь для М-М через сериализатор таблицы-связки для получения доп инфы

    class Meta:
        model = Order
        fields = ('id', 'state', 'fixed_amount', 'user', 'items')
