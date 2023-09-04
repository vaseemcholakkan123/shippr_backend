from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()


class Order(models.Model):

    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    product = models.ForeignKey("Products.product", on_delete=models.SET_NULL , null=True)
    quantity = models.PositiveSmallIntegerField(default=1)
    total_price = models.PositiveIntegerField()
    purchased_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100 , choices=(("Pending","Pending"),("Shipped","Shipped"),("Delivered","Delivered")) , default="Pending")


