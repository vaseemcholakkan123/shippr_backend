from django.test import TestCase, Client
from django.urls import reverse, resolve
from Auth.models import User
from django.contrib.auth.hashers import make_password
from Auth.views import VendorLogin,UserLogin
import json



class TestAuthViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.vendor_login_url = reverse("vendor-login")
        self.login_url = reverse("login")
        self.test_user = User.objects.create(username="test_user" , password=(make_password("1234")) , is_vendor= False)

    def test_login_without_credentials(self):
        response = self.client.post(self.login_url,data={})
        self.assertEquals(response.status_code , 400)

    def test_vendor_login_as_not_vendor(self):
        data = {
            "username" : self.test_user.username,
            "password" : "1234",
        }

        response = self.client.post(self.vendor_login_url , data=data)

        response_data = json.loads(response.content.decode('utf-8'))
        response_message = response_data.get("message")

        self.assertEquals( response_message, "User not Vendor")
        self.assertEquals( response.status_code, 401)




