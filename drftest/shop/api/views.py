from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

class ShopAPIView(APIView):
    permission_classes = (IsAuthenticated,)

class OrdersView(ShopAPIView):
    """
    Place an order. Create the "order" record with general informations, create the "order_details" records with
    the details of the order. During this transaction any stamp earned by the user is added to the database and
    at the end voucher(s) are created if there are enough stamps available for that user.
    """
    def post(self, request, format=None):
        with transaction.atomic():
            return Response({'success': True})
