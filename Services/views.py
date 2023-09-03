from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from . import serializers as ServiceSerializers
from Products.models import  Product
from Products.mixins import UserInSerializerContext
from Products.views import NormalPagination
# Create your views here.


class PurchaseProducts(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_list = request.data

        for order in order_list:
            product = order["product"]
            quantity = order['quantity']

            if not quantity:
                return  Response(status=status.HTTP_400_BAD_REQUEST , data={"message" : "No quantity provided"})

            product = Product.objects.filter(id=product)

            if not product or isinstance(product , int):
                return  Response(status=status.HTTP_400_BAD_REQUEST , data={"message" : "No product with this id"})

            product = product.first()
            total_price = quantity * product.price
            ord = Order.objects.create(user=request.user ,product=product,quantity=quantity , total_price=total_price)
            print("creaeteing" , ord)

        return Response(status=status.HTTP_201_CREATED)


class GetUserOrders(UserInSerializerContext, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ServiceSerializers.UserOrderSerializer
    pagination_class = NormalPagination

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


