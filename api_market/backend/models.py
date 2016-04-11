from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    """Пользователи системы."""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    sex = models.CharField(max_length=6, blank=True)
    address = models.CharField(max_length=255, blank=True)
    auth_time = models.DateTimeField(auto_now_add=True)
    request_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class Product(models.Model):
    """Товары."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.IntegerField()
    is_active = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    # catalog = models.ForeignKey(CatalogProduct)

    def __str__(self):
        return self.title


class Order(models.Model):
    """Заказы (Корзина)."""
    """Статусы заказов. Изменяются в зависимости действий пользователя или менеджера."""
    STATE_CART = 1
    STATE_CONFIRMED = 2
    STATE_SHIPPING = 3
    STATE_CANCEL = 4
    STATE_COMPLETE = 5

    STATES = (
        (STATE_CART, "Корзина"),
        (STATE_CONFIRMED, "На обработке"),
        (STATE_SHIPPING, "Отправлен"),
        (STATE_CANCEL, "Отменен"),
        (STATE_COMPLETE, "Завершен"),
    )

    products = models.ManyToManyField(Product, through='OrderProduct')
    user = models.ForeignKey(User)
    state = models.IntegerField(default=STATE_CART, choices=STATES)
    fixed_amount = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def get_cart(self, user):
        """Вернет модель заказа в статусе для корзины."""
        try:
            order = Order.objects.get(user=user, state=self.STATE_CART)
        except self.DoesNotExist:
            # Создание новой корзины.
            order = Order(user=user, state=self.STATE_CART)
            order.save()
        except self.MultipleObjectsReturned:
            # Фикс если у пользователя оказывается несколько корзин.
            orders = Order.objects.filter(user=user, state=self.STATE_CART).all()
            order = orders.last()
            for broken_order in orders:
                if order != broken_order:
                    broken_order.delete()
        return order

    def __str__(self):
        return '#' + str(self.id) + ' от ' + str(self.user) + ' на сумму ' + str(self.fixed_amount) + ' статус ' + str(dict(self.STATES)[self.state])


class OrderProduct(models.Model):
    """Товары в заказах."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count_product = models.IntegerField(default=1)


class Catalog(models.Model):
    """Каталоги товаров."""
    alias = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()


class CatalogProduct(models.Model):
    """Закрепление товаров за каталогом.

    Связь между каталогом и товаром 1-М можно обеспечить наличием соответствующего поля в модели Product,
       однако данный вариант позволяет избавиться от null значений у товаров без категории. Кроме того
       в данном виде возможен переход к связи М-М тем самым обеспечив нахождение товара в нескольких каталогах.

    """
    product = models.OneToOneField(Product)
    catalog = models.ForeignKey(Catalog)
