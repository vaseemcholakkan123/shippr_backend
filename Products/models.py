from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)


class Product(models.Model):

    vendor = models.ForeignKey(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    posted_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category , on_delete=models.SET_NULL , null=True)


class Images(models.Model):

    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')





class CartItem(models.Model):

    user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)