from rest_framework import serializers
from shop.models import Product, Voucher

class OrderSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_product(self, value):
        if value:
            if Product.objects.filter(id=value).count() == 0:
                raise serializers.ValidationError('Invalid product: {0}'.format(value))

        return value

class VoucherSerializer(serializers.Serializer):
    voucher = serializers.IntegerField()

    def validate_voucher(self, value):
        if value:
            if Voucher.objects.filter(id=value).count() == 0:
                raise serializers.ValidationError('Invalid voucher: {0}'.format(value))

        return value
