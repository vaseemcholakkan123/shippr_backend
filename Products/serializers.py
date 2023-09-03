from . import models as ProductModels
from rest_framework import serializers
from Auth.serializers import UserSerializer
from django.contrib.auth.models import AnonymousUser



class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModels.Images
        fields = ('image',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModels.Category
        fields = '__all__'


class CreateProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = ProductModels.Product
        fields = '__all__'

    def get_images(self ,ProductObj):
        images = ProductModels.Images.objects.filter(product=ProductObj)
        images = ImageSerializer(images , many=True).data
        images = [imageOBJ['image'] for imageOBJ in images]
        return images

    def create(self, validated_data):
        images = self.initial_data.get("images", None)

        if not images:
            raise serializers.ValidationError({"message": "No images Provided"})

        product = super().create(validated_data)

        for img in images:
            ProductModels.Images.objects.create(product=product, image=img)

        return product

class ProductSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()
    category = CategorySerializer(many=False)
    vendor = UserSerializer(many=False)
    is_in_cart = serializers.SerializerMethodField()

    class Meta:
        model = ProductModels.Product
        fields = '__all__'

    def get_images(self ,ProductObj):
        images = ProductModels.Images.objects.filter(product=ProductObj)
        images = ImageSerializer(images , many=True).data
        images = [imageOBJ['image'] for imageOBJ in images]
        return images


    def get_is_in_cart(self , ProdOBJ):
        user = self.context['user']
        if isinstance(user, AnonymousUser):
            return False
        return ProductModels.CartItem.objects.filter(user=user, product= ProdOBJ).exists()


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = ProductModels.CartItem
        fields = '__all__'







