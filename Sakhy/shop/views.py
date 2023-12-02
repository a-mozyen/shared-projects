from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from .serializers import StoreSerializer, CouponSerializer, OrderSerializer
from .models import Store, Coupon, Order
from user.models import User
from user.authentications import CustomAuthentication
from rest_framework.permissions import IsAuthenticated


class StoresList(APIView):
    def get(self, request):
        try:
            stores = Store.objects.all()
            serializer = StoreSerializer(instance=stores, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            raise exceptions.APIException(detail=serializer.errors, code=status.HTTP_400_BAD_REQUEST)
        
class StoreCoupons(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]
    def get(self, request, store_id):
        try:
            coupons = Coupon.objects.filter(store_id=store_id)
            serializer = CouponSerializer(instance=coupons, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            raise exceptions.APIException(detail=serializer.errors, code=status.HTTP_400_BAD_REQUEST)

class Orders(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]
    def post(self, request, coupon_id):
        user = User.objects.get(id=request.user.id)
        coupon = Coupon.objects.get(coupon_id=coupon_id)
        store = coupon.store_id

        if not user:
            raise exceptions.APIException(detail='Error retrieving user data')
        
        if not coupon:
            raise exceptions.APIException(detail='Coupon not found')
        
        
        if user.wallet >= coupon.coupon_price:
            user.wallet -= coupon.coupon_price
            user.save()
        else:
            raise exceptions.APIException(detail='Insufficient funds in your wallet')
        
        order_amount = request.data.get('order_amount')
        if not order_amount:
            order_amount = 1

        order = Order.objects.create(
            user_id=user, 
            store_id=store,
            coupon_id=coupon, 
            order_amount=order_amount
            )
        
        serializer = OrderSerializer(instance=order)
        return Response(data=serializer.data)
    
class UserOrders(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.id)
        serializer = OrderSerializer(orders, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        