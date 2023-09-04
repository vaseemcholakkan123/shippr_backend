from django.test import TestCase, Client
from Products.models import Category , Product
from Auth.models import User
from django.contrib.auth.hashers import make_password
from django.urls import reverse
import json


class TestProductActions(TestCase):

    def setUp(self) -> None:
        self.product_action_url = reverse('product-action')
        self.test_user_vendor = User.objects.create(username="test_user", password=(make_password("1234")), is_vendor=True)
        self.test_user_not_vendor = User.objects.create(username="test_user2", password=(make_password("1234")), is_vendor=False)
        self.test_user_different_vendor = User.objects.create(username="test_user3", password=(make_password("1234")), is_vendor=True)
        self.client = Client()


    def ClientAsVendor(self):
        token_response = self.client.post(reverse("login"), data={"username": "test_user", "password": "1234"})
        response_data = json.loads(token_response.content.decode('utf-8'))
        access_token = response_data.get("access_token")

        return access_token

    def ClientAsDifferentVendor(self):
        token_response = self.client.post(reverse("login"), data={"username": "test_user3", "password": "1234"})
        response_data = json.loads(token_response.content.decode('utf-8'))
        access_token = response_data.get("access_token")

        return access_token

    def ClientAsNotVendor(self):
        token_response = self.client.post(reverse("login"), data={"username": "test_user2", "password": "1234"})
        response_data = json.loads(token_response.content.decode('utf-8'))
        access_token = response_data.get("access_token")

        return access_token

    def test_no_image_product_creation(self):

        Category.objects.create(name="test_category",id=1)

        access_token = self.ClientAsVendor()
        data = {
            "name" : "shirt blue",
            "description" : "test description",
            "category" : "1",
            "price" : 200,
        }

        response = self.client.post(self.product_action_url ,data=data ,headers={"Authorization" : "Bearer " + access_token})
        response_data = json.loads(response.content.decode('utf-8'))
        response_message = response_data.get("message")

        self.assertEquals(response_message , "No images Provided")
        self.assertEquals(response.status_code, 400)

    def test_user_not_vendor_product_creation(self):
        Category.objects.create(name="test_category", id=1)

        access_token = self.ClientAsNotVendor()
        data = {
            "name": "shirt blue",
            "description": "test description",
            "category": "1",
            "price": 200,
        }

        response = self.client.post(self.product_action_url ,data=data ,headers={"Authorization" : "Bearer " + access_token})

        response_data = json.loads(response.content.decode('utf-8'))
        response_detail = response_data.get("detail")

        self.assertEquals(response.status_code , 403)
        self.assertEquals( response_detail, "You do not have permission to perform this action.")

    def test_user_not_owner_product_update(self):
        test_category = Category.objects.create(name="test_category", id=1)
        product = Product.objects.create(id=1,name="test_product" , description="test_description", price=100 , category=test_category, vendor=self.test_user_vendor)

        access_token = self.ClientAsDifferentVendor()
        response = self.client.patch(reverse('product-action',kwargs={ "pk" : 1 }) ,
                                     data={"name" : "change_to_name"} ,
                                     headers={"Authorization" : "Bearer " + access_token},
                                     content_type = 'application/json',
                                    )

        response_data = json.loads(response.content.decode('utf-8'))
        response_detail = response_data.get("detail")

        self.assertEquals(response.status_code, 403)
        self.assertEquals(response_detail, "You do not have permission to perform this action.")


