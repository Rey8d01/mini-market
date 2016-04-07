from rest_framework import viewsets
from .serializers import ItemSerializer, OrderSerializer
from .models import Item, Order, User


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def get_queryset(self):
    #     # Order.objects.filter(user=).all()
    #     Order.objects.all()
    #     queryset = super(UserPostList, self).get_queryset()
    #     return queryset.filter(author__username=self.kwargs.get('username'))


class CartViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
