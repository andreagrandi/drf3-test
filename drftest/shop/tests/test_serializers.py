from django.test import TestCase
from .factories import ProductFactory, UserFactory, VoucherFactory
from shop.api.serializers import OrderSerializer, VoucherSerializer

class ShopOrderSerializerTestCase(TestCase):
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


class ShopVoucherSerializer(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.voucher = VoucherFactory(user=self.user)

    def test_voucher_serializer_valid_voucher(self):
        data  = {'voucher': self.voucher.id}
        serializer = VoucherSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_voucher_serializer_invalid_voucher(self):
        data  = {'voucher': 'abc123'}
        serializer = VoucherSerializer(data=data)
        self.assertFalse(serializer.is_valid())
