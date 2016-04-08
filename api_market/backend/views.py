from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import ItemSerializer, OrderSerializer, UserSerializer
from .models import Item, Order, User
from django.contrib.auth import login, logout, authenticate


class ItemViewSet(viewsets.ModelViewSet):
    """Список товаров в каталоге."""
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(is_active=True)


class OrdersViewSet(viewsets.ModelViewSet):
    """Список заказов пользователя."""
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


class CartViewSet(viewsets.ModelViewSet):
    """Список товаров в корзине."""
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user, state=Order.STATE_CART)


# ААА
class AuthView(APIView):

    def put(self, request, *args, **kwargs):
        """Регистрация"""
        email = self.request.data["email"]
        password = self.request.data["password"]
        password_confirm = self.request.data["passwordConfirm"]

        if password == password_confirm:
            user = User(email=email)
        else:
            raise exceptions.NotAuthenticated('wrong password')

        user.set_password(password)
        user.full_clean()
        user.save()

        user.backend = 'backend.backends.ModelBackend'
        login(request, user)
        return Response({'auth': UserSerializer(request.user).data})

    def post(self, request, *args, **kwargs):
        """Авторизация"""
        email = self.request.data["email"]
        password = self.request.data["password"]

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"auth": UserSerializer(request.user).data})
        else:
            raise exceptions.NotAuthenticated('wrong password or email')

    def delete(self, request, *args, **kwargs):
        """Выход"""
        logout(request)
        return Response({})
