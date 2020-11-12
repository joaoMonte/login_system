from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, Phone
import json


class TestSignup(TestCase):

    def test_insert_correct_user(self):
        new_user = {
            "firstName": "joao",
            "lastName": "monte",
            "email": "joao.monte@joao.com",
            "password": "helloworld",
            "phones": [
                {
                    "number": "12345678",
                    "area_code": "81",
                    "country_code": "+55"
                },
                {
                    "number": "87654321",
                    "area_code": "81",
                    "country_code": "+55"
                }
            ]
        }
        response = self.client.post(reverse("signup"), 
                                    json.dumps(new_user),
                                    content_type="application/json")
        user = User.objects.get(email=new_user["email"])
        phones = Phone.objects.filter(ownerEmail = new_user["email"])
        
        assert "token" in response.json()
        assert user.firstName == new_user["firstName"] 
        assert user.lastName == new_user["lastName"] 
        assert user.password == new_user["password"]
        assert phones.count() == 2

    def test_insert_user_empty_name(self):
        new_user = {
            "firstName": "",
            "lastName": "monte",
            "email": "joao@joao.com",
            "password": "helloworld",
            "phones": [
                {
                    "number": "12345678",
                    "area_code": "81",
                    "country_code": "+55"
                },
                {
                    "number": "87654321",
                    "area_code": "81",
                    "country_code": "+55"
                }
            ]
        }
        response = self.client.post(reverse("signup"),
                                    json.dumps(new_user),
                                    content_type="application/json")
        assert "Validation Error" in response.json()

    def test_insert_user_invalid_name(self):
        new_user = {
            "firstName": 2,
            "lastName": "monte",
            "email": "joao@joao.com",
            "password": "helloworld",
            "phones": [
                {
                    "number": "12345678",
                    "area_code": "81",
                    "country_code": "+55"
                },
                {
                    "number": "87654321",
                    "area_code": "81",
                    "country_code": "+55"
                }
            ]
        }
        response = self.client.post(reverse("signup"),
                                    json.dumps(new_user),
                                    content_type="application/json")
        assert "Validation Error" in response.json()

    def test_insert_user_invalid_email(self):
        new_user = {
            "firstName": "joao",
            "lastName": "monte",
            "email": "joao@joao.com",
            "password": "helloworld",
            "phones": [
                {
                    "number": "12345678",
                    "area_code": "81",
                    "country_code": "+55"
                },
                {
                    "number": "87654321",
                    "area_code": "81",
                    "country_code": "+55"
                }
            ]
        }
        invalid_mails = [
            "@joao.com", "Joao@gmail.com", "$%&@gmail.com", "joao@gmail",
            "joao", "joao@%#$%"
        ]
        for invalid_mail in invalid_mails:
            new_user["email"] = invalid_mail
            response = self.client.post(reverse("signup"),
                                        json.dumps(new_user),
                                        content_type="application/json")
            assert "Validation Error" in response.json()

    def test_insert_user_without_phones(self):
        new_user = {
            "firstName": "joao",
            "lastName": "monte",
            "email": "joao@joao.com",
            "password": "helloworld",
            "phones": []
        }
        response = self.client.post(reverse("signup"),
                                    json.dumps(new_user),
                                    content_type="application/json")
        assert "Validation Error" in response.json()
    
    def test_insert_user_invalid_phone_number(self):
        new_user = {
            "firstName": "joao",
            "lastName": "monte",
            "email": "joao@joao.com",
            "password": "helloworld",
            "phones": [
                {
                    "number": "a12345678",
                    "area_code": "81",
                    "country_code": "+55"
                },
                {
                    "number": "87654321",
                    "area_code": "81",
                    "country_code": "+55"
                }
            ]
        }
        response = self.client.post(reverse("signup"),
                                    json.dumps(new_user),
                                    content_type="application/json")
        assert "Validation Error" in response.json()
    
    def test_insert_user_invalid_phone_area_code(self):
        new_user = {
            "firstName": "joao",
            "lastName": "monte",
            "email": "joao@joao.com",
            "password": "helloworld",
            "phones": [
                {
                    "number": "12345678",
                    "area_code": "a81",
                    "country_code": "+55"
                },
                {
                    "number": "87654321",
                    "area_code": "81",
                    "country_code": "+55"
                }
            ]
        }
        response = self.client.post(reverse("signup"),
                                    json.dumps(new_user),
                                    content_type="application/json")
        assert "Validation Error" in response.json()

    def test_insert_user_invalid_phone_country_code(self):
        new_user = {
            "firstName": "joao",
            "lastName": "monte",
            "email": "joao@joao.com",
            "password": "helloworld",
            "phones": [
                {
                    "number": "12345678",
                    "area_code": "a81",
                    "country_code": "+55"
                },
                {
                    "number": "87654321",
                    "area_code": "81",
                    "country_code": "55"
                }
            ]
        }
        response = self.client.post(reverse("signup"),
                                    json.dumps(new_user),
                                    content_type="application/json")
        assert "Validation Error" in response.json()


