from .models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework import status



class AuthMixin:
    is_vendor_login = False

    def authenticate_login(self,request):
        username = request.data.pop("username", None)
        password = request.data.pop("password", None)

        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Credentials not provided'})

        user = authenticate(username=username, password=password)

        if user:

            if self.is_vendor_login and not user.is_vendor:
                return Response(status=status.HTTP_401_UNAUTHORIZED , data= { "message" : "User not Vendor"})

            auth_tokens = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "user": user_data,
                    "access_token": str(auth_tokens.access_token),
                    "refresh_token": str(auth_tokens),
                }
            )

        else:

            try:
                User.objects.get(username=username)
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={"message": "Password Wrong !"},
                )

            except User.DoesNotExist:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": "No User with this credentials !"},
                )
