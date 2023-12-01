from django.urls import path
from .views import StoresList, StoreCoupons, Orders


urlpatterns = [
    path('stores/', StoresList.as_view(), name='stores list'),
    path('coupons/<int:store_id>', StoreCoupons.as_view(), name='coupons'),
    path('order/<int:coupon_id>', Orders.as_view(), name='order'),
]