from django.contrib.auth.models import User
from django.utils import timezone
from djongo.models import ObjectIdField
from django.db import models
from .choices import ORDER_TYPE, STATUS_TYPE
import random


class Profile(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    btc = models.IntegerField(default=random.randint(1, 10), null=True)


class Order(models.Model):
    _id = ObjectIdField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now())
    type = models.IntegerField(choices=ORDER_TYPE, null=True)
    price = models.FloatField(null=True)
    quantity = models.FloatField(null=True)
    status = models.IntegerField(choices=STATUS_TYPE, null=True)
    earning = models.FloatField(null=True)
