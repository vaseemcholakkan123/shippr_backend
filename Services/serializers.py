from rest_framework import serializers
from . import models as ServiceModels
from Products.serializers import ProductSerializer,UserSerializer
from Products.models import Product



class UserOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = ServiceModels.Order
        fields = '__all__'


class VendorOrderSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    user = UserSerializer(many=False)
    class Meta:
        model = ServiceModels.Order
        fields = '__all__'

    def get_product(self , OrderOBJ):
        product = Product.objects.filter(id=OrderOBJ.product.id)

        if product.exists():
            product = product.first()
            product = {
                "name" : product.name,
                "id" : product.id,
            }
        else:
            product = {
                "name": "deleted product",
                "id": 0
            }

        return product