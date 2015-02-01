import factory
from django.contrib.auth.models import User
from django.utils.timezone import now
from shop.models import (Product, Stamp, Order, OrderDetails, Voucher)


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    first_name = 'DRF'
    last_name = 'Test'
    username = 'drftest'
    password = 'drftest'
    is_active = True
    is_superuser = False
    last_login = now()
    date_joined = now()


class ProductFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Product

    name = "Product 1"
    collect_stamp = True


class StampFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Stamp

    user = factory.SubFactory(UserFactory)
    redeemed = False


class OrderFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Order

    user = factory.SubFactory(UserFactory)
    date = now()


class OrderDetailsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = OrderDetails

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 4


class VoucherFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Voucher

    user = factory.SubFactory(UserFactory)
    redeemed = False
