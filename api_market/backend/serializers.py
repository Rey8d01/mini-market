"""Сериализаторы для API."""
from rest_framework import serializers
from .models import Product, Order, User, OrderProduct, Catalog


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ('id', 'title', 'alias', 'description')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'amount')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'sex', 'address')


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    title = serializers.ReadOnlyField(source='product.title')
    amount = serializers.ReadOnlyField(source='product.amount')

    class Meta:
        model = OrderProduct
        fields = ('id', 'title', 'amount', 'count_product')


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    # Связь для М-М
    # products = ProductSerializer(many=True)
    # Связь для М-М через сериализатор таблицы-связки для получения доп инфы
    products = OrderItemSerializer(source='orderproduct_set', many=True)

    class Meta:
        model = Order
        fields = ('id', 'state', 'fixed_amount', 'user', 'products', 'create_time')
