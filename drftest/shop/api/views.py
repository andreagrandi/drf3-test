from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db import transaction
from django.utils.timezone import now
from .serializers import OrderSerializer
from shop.models import Order, OrderDetails, Product, Stamp, Voucher

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
            data = JSONParser().parse(request)
            serializer = OrderSerializer(data=data, many=True)

            if serializer.is_valid():
                order = Order()
                order.user = request.user
                order.date = now()
                order.save()

                for d in serializer.data:
                    product = Product.objects.get(id=d['product'])
                    detail = OrderDetails()
                    detail.order = order
                    detail.product = product
                    detail.quantity = d['quantity']
                    detail.save()

                    # Collect stamps here
                    if product.collect_stamp:
                        for i in xrange(detail.quantity):
                            Stamp(user=request.user).save()

                # Generate Vouchers
                vouchers_to_create = Stamp.objects.filter(
                    user=request.user, redeemed=False).count() // 10

                for i in xrange(vouchers_to_create):
                    Voucher(user=request.user).save()
                    stamps_to_use = Stamp.objects.filter(
                        user=request.user, redeemed=False).values('pk')[:10]
                    Stamp.objects.filter(pk__in=stamps_to_use).update(redeemed=True)

                return Response({'success': True})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
