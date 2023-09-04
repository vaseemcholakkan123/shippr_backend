from rest_framework.views import APIView
from rest_framework import generics , status
from rest_framework import permissions
from rest_framework.response import Response
from .models import User
from .serializers import CreateUserSerializer , UserSerializer
from .mixins import AuthMixin

# Create your views here.


class RegisterUser(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    model = User
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_201_CREATED)


class UserLogin(AuthMixin ,APIView):
    permission_classes = [permissions.AllowAny]

    def post(self , request , *args , **kwargs):
        return self.authenticate_login(request)


class RegisterAsVendor(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request , *args , **kwargs):
        user = self.request.user
        user.is_vendor = True
        user.save()
        return Response(status=status.HTTP_200_OK)


class VendorLogin(AuthMixin, APIView):
    permission_classes = [permissions.AllowAny]
    is_vendor_login = True

    def post(self, request, *args, **kwargs):
        return self.authenticate_login(request)


class GetAllVendors(generics.ListAPIView):
    permission_classes =  [permissions.AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_vendor=True)