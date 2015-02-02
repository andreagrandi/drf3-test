from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.test import TestCase
from .factories import UserFactory, ProductFactory, StampFactory, VoucherFactory
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetails.objects.count(), 2)
        self.assertEqual(Stamp.objects.count(), 26)
        self.assertEqual(Stamp.objects.filter(redeemed=False).count(), 6)
        self.assertEqual(Voucher.objects.count(), 2)

    def test_order_post_invalid_product(self):
        ProductFactory.create(name='Widget', collect_stamp=True)
        prod_2 = ProductFactory.create(name='Gizmo', collect_stamp=False)

        url = reverse('shop-api:shop_orders', )
        data = [{"product": 1234, "quantity": 26},
            {"product": prod_2.id, "quantity": 30}]

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_available_stamps(self):
        StampFactory.create(user=self.user, redeemed=False)
        StampFactory.create(user=self.user, redeemed=False)
        StampFactory.create(user=self.user, redeemed=False)
        StampFactory.create(user=self.user, redeemed=False)
        StampFactory.create(user=self.user, redeemed=True)
        StampFactory.create(user=self.user, redeemed=True)

        url = reverse('shop-api:shop_stamps', )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stamps'], 4)

    def test_add_stamp_to_user(self):
        url = reverse('shop-api:shop_stamps', )
        response = self.client.post(url, format='json')
        self.assertEqual(Stamp.objects.count(), 1)
        self.assertEqual(response.data['success'], True)
        self.assertTrue(response.data['stamp'] > 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_available_vouchers(self):
        VoucherFactory.create(user=self.user, redeemed=False)
        VoucherFactory.create(user=self.user, redeemed=False)
        VoucherFactory.create(user=self.user, redeemed=False)
        VoucherFactory.create(user=self.user, redeemed=True)
        VoucherFactory.create(user=self.user, redeemed=True)

        url = reverse('shop-api:shop_vouchers', )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vouchers'], 3)

    def test_add_voucher_to_user(self):
        url = reverse('shop-api:shop_vouchers', )
        response = self.client.post(url, format='json')
        self.assertEqual(Voucher.objects.count(), 1)
        self.assertEqual(response.data['success'], True)
        self.assertTrue(response.data['voucher'] > 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mark_voucher_redeemed(self):
        voucher = VoucherFactory.create(user=self.user)
        url = reverse('shop-api:shop_vouchers', )
        data = {'voucher': voucher.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        voucher_modified = Voucher.objects.get(id=voucher.id)
        self.assertEqual(voucher_modified.redeemed, True)
