from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import exceptions, viewsets, generics, permissions
from .serializers import ProductSerializer, OrderSerializer, UserSerializer, CatalogSerializer, TagSerializer
from .models import Product, Order, User, OrderProduct, Catalog, Tag
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AnonymousUser


class ProductResultsSetPagination(PageNumberPagination):
    """Перекрытие класса постраничной навигации для продуктов."""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class CatalogListViewSet(viewsets.ReadOnlyModelViewSet):
    """Список каталогов."""
    serializer_class = CatalogSerializer
    queryset = Catalog.objects.filter()


class CatalogItemViewSet(viewsets.ReadOnlyModelViewSet):
    """Информация по каталогу."""
    serializer_class = CatalogSerializer
    lookup_field = 'alias'
    queryset = Catalog.objects


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Список всех тегов."""
    serializer_class = TagSerializer
    queryset = Tag.objects.filter()


class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    """Список товаров в каталоге."""
    serializer_class = ProductSerializer
    pagination_class = ProductResultsSetPagination

    def get_queryset(self):
        alias = self.kwargs["alias"]
        try:
            tags = self.request.query_params["tags"]
            return Product.objects.filter(is_active=True, catalog__alias=alias, tags__alias=tags)
        except KeyError:
            return Product.objects.filter(is_active=True, catalog__alias=alias)


class OrderViewSet(viewsets.ModelViewSet):
    """Список заказов пользователя."""
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user).exclude(state=Order.STATE_CART).order_by('-create_time')

    def delete(self, request, *args, **kwargs):
        """Отмена заказа, если он еще не отправлен."""
        order_id = int(kwargs["order_id"])
        order = Order.objects.get(id=order_id, user=self.request.user, state=Order.STATE_CONFIRMED)
        order.state = Order.STATE_CANCEL
        order.save()
        return Response(OrderSerializer(order).data)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """Информация об авторизованном пользователе."""
    model = User
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.request.user


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    """API работы с корзиной."""
    model = Order
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, *args, **kwargs):
        """Добавление товара в корзину."""
        product = self.request.data["product"]
        try:
            change = int(self.request.data["change"])
        except KeyError:
            change = 1
        product = Product.objects.get(pk=product)
        cart = self.get_object()

        try:
            order_product = OrderProduct.objects.get(order=cart, product=product)
            order_product.count_product += change
        except OrderProduct.DoesNotExist:
            order_product = OrderProduct(order=cart, product=product)

        if order_product.count_product <= 0:
            order_product.delete()
        else:
            order_product.save()

        return Response(OrderSerializer(cart).data)

    def put(self, request, *args, **kwargs):
        """Подтверждение статуса заказа пользователем."""
        cart = self.get_object()
        amount = sum([item_orderproduct.product.amount * item_orderproduct.count_product for item_orderproduct in cart.orderproduct_set.all()])
        if amount:
            cart.fixed_amount = amount
            cart.state = Order.STATE_CONFIRMED
            cart.save()
        else:
            raise exceptions.APIException("Ошибка при формировании заказа")
        return Response(OrderSerializer(cart).data)

    def get_queryset(self):
        """Получение товаров в заказе авторизованного пользователя."""
        user = self.request.user
        return Order.objects.filter(user=user)

    def get_object(self):
        """Получение товаров в заказе со статусом 1 для авторизованного пользователя."""
        user = self.request.user
        return Order().get_cart(user)


class AuthView(APIView):
    """AAA"""

    def get(self, request, *args, **kwargs):
        """Получение информации по авторизованному пользователю."""
        if isinstance(request.user, AnonymousUser):
            return Response({'auth': ""})
        return Response({'auth': UserSerializer(request.user).data})

    def put(self, request, *args, **kwargs):
        """Регистрация."""
        email = self.request.data["email"]
        password = self.request.data["password"]
        password_confirm = self.request.data["passwordConfirm"]

        # Проверка совпадения значений пароля и подтверждение пароля.
        if password == password_confirm:
            user = User(email=email)
        else:
            raise exceptions.NotAuthenticated("Поля подтверждение и пароль не совпдают")

        user.set_password(password)
        user.full_clean()
        user.save()

        # Авторизация сразу после регистрации.
        user.backend = 'backend.backends.ModelBackend'
        login(request, user)
        return Response({'auth': UserSerializer(request.user).data})

    def post(self, request, *args, **kwargs):
        """Авторизация."""
        email = self.request.data["email"]
        password = self.request.data["password"]

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"auth": UserSerializer(request.user).data})
        else:
            raise exceptions.NotAuthenticated("Ошибка в email или пароле")

    def delete(self, request, *args, **kwargs):
        """Выход."""
        logout(request)
        return Response({})
