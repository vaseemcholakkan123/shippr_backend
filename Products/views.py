from rest_framework.views import APIView
from rest_framework import generics , status, permissions , pagination
from rest_framework.response import Response
from . import serializers as ProductsSerializers
from .models import Product,Category,CartItem
from .permissions import IsVendorOrReadOnly
from .mixins import UserAsVendorAPIView,UserInSerializerContext

# Create your views here.

class NormalPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200

class ProductActionVendor(UserAsVendorAPIView):
    permission_classes = [IsVendorOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductsSerializers.CreateProductSerializer


class RetrieveVendorProducts(UserInSerializerContext, generics.ListAPIView):
    pagination_class = NormalPagination
    permission_classes = [IsVendorOrReadOnly]
    serializer_class = ProductsSerializers.ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user)


class GetCategories(generics.ListAPIView):
    serializer_class = ProductsSerializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()


class GetProductForUser(UserInSerializerContext ,generics.ListAPIView):
    pagination_class = NormalPagination
    serializer_class =  ProductsSerializers.ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.AllowAny]

class GetUserCart(UserInSerializerContext, generics.ListAPIView):
    pagination_class = NormalPagination
    serializer_class = ProductsSerializers.CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class AddOrRemoveCart(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self , request , *args , **kwargs):
        product_id = kwargs.get("prod_id",None)

        if not product_id:
            return  Response(status=status.HTTP_400_BAD_REQUEST)

        is_in_cart =  CartItem.objects.filter(user=request.user,product_id=product_id)

        if is_in_cart.exists():
            is_in_cart.delete()
            return  Response(status=status.HTTP_200_OK)

        CartItem.objects.create(user=request.user,product_id=product_id)
        return Response(status=status.HTTP_200_OK)


class ProductDetailView(UserInSerializerContext, generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductsSerializers.ProductSerializer
    queryset = Product.objects.all()



