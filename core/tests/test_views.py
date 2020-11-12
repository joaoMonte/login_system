from django.test import TestCase, Client
from django.urls import reverse
import json


class TestSignup(TestCase):

    def test_insert_correct_user(self):
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
        response = self.client.post(reverse("signup"), json.dumps(new_user), content_type="application/json")
        assert response.status_code == 200
        assert "token" in response.json()



