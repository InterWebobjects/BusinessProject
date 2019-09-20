from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
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
class User(AbstractUser):
    uid = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=128, unique=True, null=False)
    mobile = models.CharField(max_length=16, null=True)
    gender = models.IntegerField(blank=True, null=True, default=1)
    password_hash = models.CharField(max_length=128, db_column='password', null=True)
    type = models.IntegerField(blank=True, null=True, default=0)
    score = models.IntegerField(blank=True, null=True, default=0)
    birthday = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    last_login = models.DateTimeField(null=True)

    class Meta:
        managed = True
        db_table = 'b2c_user'

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = make_password(value)

    def verify_password(self, password):
        return check_password(password, self.password_hash)

    @classmethod
    def check_login(cls, email, password):
        user = cls.objects.filter(email=email).first()
        if user and user.verify_password(password):
            return user
        return False


# 手表
class Commodity(models.Model):
    cname = models.CharField(max_length=128)
    picture_1 = models.CharField(max_length=256)
    picture_2 = models.CharField(max_length=256)
    picture_3 = models.CharField(max_length=256)
    tag = models.CharField(max_length=16)
    sku = models.CharField(max_length=32)
    description = models.CharField(max_length=128, null=True)
    plate = models.CharField(max_length=128, null=True)
    case = models.CharField(max_length=128, null=True)
    gem = models.CharField(max_length=128, null=True)
    strap = models.CharField(max_length=128, null=True)
    price = models.CharField(max_length=16)
    sid = models.ForeignKey(Style, models.CASCADE, db_column='sid', blank=True, null=True)
    is_delete = models.IntegerField(default=0)
    watch = models.CharField(max_length=128, null=True)

    class Meta:
        managed = True
        db_table = 'b2c_commodity'


# 购物车
class Cart(models.Model):
    count = models.IntegerField()
    cid = models.ForeignKey(Commodity, models.CASCADE, db_column='cid')
    uid = models.ForeignKey(User, models.CASCADE, db_column='uid')


# 订单
class Order(models.Model):
    number = models.CharField(max_length=32)
    money = models.IntegerField()
    create_time = models.DateTimeField(blank=True, null=True)
    pay_time = models.DateTimeField(blank=True, null=True)
    send_time = models.DateTimeField(blank=True, null=True)
    uid = models.ForeignKey(User, models.CASCADE, db_column='uid', blank=True, null=True)
    cid = models.ForeignKey(Commodity, models.CASCADE, db_column='cid', blank=True, null=True)
    is_delete = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'b2c_order'
