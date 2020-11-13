from django.test import TestCase, Client
from django.urls import reverse
import jwcrypto.jwk as jwk
from ..models import User, Phone
from ..utils import generateToken
import json


class TestMe(TestCase):
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

    def setUp(self):
        session = self.client.session
        session["key_json"] = jwk.JWK.generate(kty='oct', size=256).export()
        session.save()
        

    def test_auth_correct_user(self):
        key = jwk.JWK.from_json(self.client.session["key_json"])

        user = {
            "email": "joao.monte@joao.com",
            "password": "helloworld",
        }

        correct_output = {
            'firstName': 'joao', 
            'phones': [
                {
                    'number': '12345678',
                    'area_code': '81',
                    'country_code': '+55'
                }, 
                {
                    'number': '87654321',
                    'area_code': '81',
                    'country_code': '+55'
                }
            ], 
            'email': 'joao.monte@joao.com',
            'lastName': 'monte'
        }

        token = generateToken(user["email"], user["password"], key)
        response = self.client.get(reverse("me"), HTTP_Authorization=token)
        assert response.json() == correct_output
    
    def test_auth_without_token(self):
        response = self.client.get(reverse("me"))
        assert response.json() == {"Error": "Unauthorized"}
