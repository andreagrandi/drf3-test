from mock import Mock, patch
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.test import TestCase
from shop.api import views

class ShopAPITestCase(TestCase):
	def setUp(self):
        self.user = self.profile.user
        self.client = APIClient()
        self.client.force_authenticate(self.user)
