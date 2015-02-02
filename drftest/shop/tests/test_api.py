from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.test import TestCase
from .factories import UserFactory, ProductFactory
from shop.models import Order, OrderDetails, Stamp, Voucher

class ShopAPITestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_order_post(self):
        prod_1 = ProductFactory.create(name='Widget', collect_stamp=True)
        prod_2 = ProductFactory.create(name='Gizmo', collect_stamp=False)

        url = reverse('shop-api:shop_orders', )
        data = [{"product": prod_1.id, "quantity": 26},
            {"product": prod_2.id, "quantity": 30}]

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetails.objects.count(), 2)
        self.assertEqual(Stamp.objects.count(), 26)
        self.assertEqual(Stamp.objects.filter(redeemed=False).count(), 6)
        self.assertEqual(Voucher.objects.count(), 2)
