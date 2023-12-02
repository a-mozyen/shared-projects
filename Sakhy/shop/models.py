from django.db import models
from user.models import User

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.store_name

class Coupon(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    coupon_price = models.FloatField()
    store_id = models.ForeignKey('Store', on_delete=models.PROTECT)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    store_id = models.ForeignKey(Store, on_delete=models.PROTECT)
    coupon_id = models.ForeignKey('Coupon', on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    order_amount = models.IntegerField(default=1)
