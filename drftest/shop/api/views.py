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
    Place an order. Create the "order" record with general informations, create the "order_details"
    records with the details of the order. During this transaction any stamp earned by the user is
    added to the database and at the end voucher(s) are created if there are enough stamps available
    for that user.

        POST:
            Example: [{"product": 1, "quantity": 26},
                        {"product": 2, "quantity": 30}]
            Response: {'success': true}

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

                # Mark as redeemed all the Stamps used to create Vouchers
                for i in xrange(vouchers_to_create):
                    Voucher(user=request.user).save()
                    stamps_to_use = Stamp.objects.filter(
                        user=request.user, redeemed=False).values('pk')[:10]
                    Stamp.objects.filter(pk__in=stamps_to_use).update(redeemed=True)

                return Response({'success': True}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StampsView(ShopAPIView):
    """
    This API method returns the total number of Stamps available for a user and allows to create
    a new one.

        GET: return the Stamps for the current user

            Example: /shop/stamps
            Response: {'stamps': 12}

        POST: Add a Stamp to the current user

            Example: /shop/stamps
            Response: {'stamp': 1, 'success': true}
    """
    def get(self, request, format=None):
        stamps = Stamp.objects.filter(user=request.user, redeemed=False).count()
        return Response({'stamps': stamps})

    def post(self, request, format=None):
        stamp = Stamp(user=request.user)
        stamp.save()
        return Response({'stamp': stamp.id, 'success': True}, status=status.HTTP_201_CREATED)


class VouchersView(ShopAPIView):
    """
    This API method returns the total number of Vouchers available for the user, allows the creation
    of a new Voucher and finally permits to mark a specific Voucher as redeemed.
    NOTE: the POST method doesn't consume any Stamps when adding a new Voucher. Stamps are consumed
        to generate a Voucher only during an Order placement. For consistency, when we manually add
        a Stamp we don't check if a widget was ordered. This check is only made during Order placement.

        GET: return the available Vouchers for the current user

            Example: /shops/vouchers
            Response: {'vouchers': 10}

        POST: add a new Voucher to the user

            Example: /shops/voucher
            Response: {'voucher': 1, 'success': true}

        PUT: mark a Voucher as redeemed

            Example: /shops/voucher
            Response: {'voucher': 1, 'success': true}
    """
    def get(self, request, format=None):
        vouchers = Voucher.objects.filter(user=request.user, redeemed=False).count()
        return Response({'vouchers': vouchers})

    def post(self, request, format=None):
        voucher = Voucher(user=request.user)
        voucher.save()
        return Response({'voucher': voucher.id, 'success': True}, status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        voucher_id = request.DATA.get('voucher')
        Voucher.objects.filter(id=voucher_id, user=request.user).update(redeemed=True)
        return Response({'voucher': voucher_id, 'success': True}, status=status.HTTP_200_OK)
