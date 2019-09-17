from datetime import datetime

from django.db import models


# Create your models here.
# 手表样式（板块）
class Style(models.Model):
    sid = models.AutoField(primary_key=True)
    s_name = models.CharField(max_length=60)
    parent_id = models.IntegerField()
    description = models.CharField(max_length=1000, blank=True, null=True)
    order_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'b2c_style'


# 用户表
class User(models.Model):
    uid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    email = models.CharField(max_length=128, unique=True, null=False)
    mobile = models.CharField(max_length=16, null=True)
    gender = models.IntegerField(blank=True, null=True, default=1)
    password = models.CharField(max_length=128)
    type = models.IntegerField(blank=True, null=True, default=0)
    is_active = models.IntegerField(blank=True, null=True)
    date_joined = models.DateTimeField(default=datetime.now())
    score = models.IntegerField(blank=True, null=True, default=0)
    birthday = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'b2c_user'


# 手表
class Commodity(models.Model):
    cname = models.CharField(max_length=128)
    picture = models.CharField(max_length=256)
    watch = models.CharField(max_length=128)
    plate = models.CharField(max_length=128)
    case = models.CharField(max_length=128)
    gem = models.CharField(max_length=128)
    strap = models.CharField(max_length=128)
    price = models.CharField(max_length=16)
    sid = models.ForeignKey(Style, models.CASCADE, db_column='sid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'b2c_commodity'


# 订单
class Order(models.Model):
    money = models.IntegerField()
    pay_time = models.DateTimeField(blank=True, null=True)
    uid = models.ForeignKey(User, models.CASCADE, db_column='uid', blank=True, null=True)
    cid = models.ForeignKey(Commodity, models.CASCADE, db_column='cid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'b2c_order'
