from rest_framework import serializers
from .models import Store, Coupon, Order

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ('store_id', 'store_name')

class CouponSerializer(serializers.ModelSerializer):
    store_id = serializers.StringRelatedField()
    class Meta:
        model = Coupon
        fields = '__all__'
        read_only_fields = ('coupon_id', 'coupon_amount', 'store_id')

class OrderSerializer(serializers.ModelSerializer):
    store_id = serializers.StringRelatedField()
    user_id = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_id', 'order_date', 'coupon_id', 'user_id')