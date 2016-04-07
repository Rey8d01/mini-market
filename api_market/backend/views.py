from rest_framework import viewsets
from .serializers import ItemSerializer, OrderSerializer
from .models import Item, Order, User


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


class CartViewSet(viewsets.ModelViewSet):
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user, state=Order.STATE_CART)
