from mock import Mock, patch
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.test import TestCase
from shop.api import views
from .factories import UserFactory

class ShopAPITestCase(TestCase):
	def setUp(self):
        self.user = UserFactory.create()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_order(self):
    	url = reverse('shop-api:shop_orders', )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
