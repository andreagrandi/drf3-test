from django.test import TestCase
from .factories import ProductFactory
from shop.api.serializers import OrderSerializer

class ShopSerializersTestCase(TestCase):
    def setUp(self):
        self.product_1 = ProductFactory(name='product_1', collect_stamp=True)
        self.product_2 = ProductFactory(name='product_2', collect_stamp=False)

    def test_order_serializer_valid_order(self):
        data = [{"product": self.product_1.id, "quantity": 26},
            {"product": self.product_2.id, "quantity": 30}]
        serializer = OrderSerializer(data=data, many=True)
        self.assertTrue(serializer.is_valid())

    def test_order_serializer_invalid_order(self):
        data = [{"product": 'abc123', "quantity": 26},
            {"product": self.product_2.id, "quantity": 30}]
        serializer = OrderSerializer(data=data, many=True)
        self.assertFalse(serializer.is_valid())
