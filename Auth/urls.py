from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from . import views as AuthViews


urlpatterns = [
    path("login/" , AuthViews.UserLogin.as_view() , name="login"),
    path("signup/", AuthViews.RegisterUser.as_view() , name="signup"),
    path("register-vendor/", AuthViews.RegisterAsVendor.as_view(), name="register_as_vendor"),
    path("vendor-login/", AuthViews.VendorLogin.as_view(), name="vendor_login")
]