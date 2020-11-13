from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, Phone
import json


class TestSignin(TestCase):
    @classmethod
    def setUpTestData(cls):
        new_user = User(firstName = "joao",
                        lastName  = "monte",
                        email     = "joao.monte@joao.com",
                        password  = "helloworld")
        new_user.save()

        new_phone1 = Phone(ownerEmail   = "joao.monte@joao.com",
                           number       = "12345678",
                           area_code    = "81",
                           country_code = "+55")
        new_phone2 = Phone(ownerEmail   = "joao.monte@joao.com",
                           number       = "87654321",
                           area_code    = "81",
                           country_code = "+55")
        new_phone1.save()
        new_phone2.save()
        

    def test_login_correct_user(self):
        user = {
            "email": "joao.monte@joao.com",
            "password": "helloworld",
        }

        response = self.client.post(reverse("signin"), 
                                    json.dumps(user),
                                    content_type="application/json")
        
        assert "token" in response.json()
        
    def test_login_user_unexistent_email(self):
        user = {
            "email": "joao1.monte@joao.com",
            "password": "helloworld",
        }
        response = self.client.post(reverse("signin"),
                                    json.dumps(user),
                                    content_type="application/json")
        assert response.json() == {"Error": "Invalid e-mail or password"}

    def test_login_user_wrong_password(self):
        user = {
            "email": "joao.monte@joao.com",
            "password": "helloworld1",
        }
        response = self.client.post(reverse("signin"),
                                    json.dumps(user),
                                    content_type="application/json")
        assert response.json() == {"Error": "Invalid e-mail or password"}


    def test_insert_user_invalid_email(self):
        user = {
            "email": "joao.monte@joao.com",
            "password": "helloworld",
        }
        invalid_mails = [
            "@joao.com", "Joao@gmail.com", "$%&@gmail.com", "joao@gmail",
            "joao", "joao@%#$%"
        ]
        for invalid_mail in invalid_mails:
            user["email"] = invalid_mail
            response = self.client.post(reverse("signin"),
                                        json.dumps(user),
                                        content_type="application/json")
            assert "Validation Error" in response.json()

    