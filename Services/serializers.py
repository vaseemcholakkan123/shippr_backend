from rest_framework import serializers
from . import models as ServiceModels
from Products.serializers import ProductSerializer,UserSerializer




class UserOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = ServiceModels.Order
        fields = '__all__'
