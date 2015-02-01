from django.test import TestCase
from shop.models import Order
from .factories import UserFactory, OrderFactory

class ShopModelsTestCase(TestCase):
    def setUp(self):
        pass

    def test_order_add(self):
        order = OrderFactory.create()
        self.assertEquals(Order.objects.count(), 1)       
