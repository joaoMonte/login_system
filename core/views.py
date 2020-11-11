import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User, Phone


# Create your views here.
@csrf_exempt
def signup(request):
    if request.method == "POST":
        user_json = json.loads(request.body.decode('UTF-8'))
        new_user = User(
            firstName = user_json["firstName"],
            lastName = user_json["lastName"],
            email = user_json["email"],
            password = user_json["password"]
        )
        for phone in user_json["phones"]:
            new_phone = Phone(
                ownerEmail = user_json["email"],
                number = user_json["phones"]["number"],
                area_code = user_json["phones"]["area_code"],
                country_code = user_json["phones"]["country_code"]
            )
        new_user.save()
        new_phone.save()

        response = {"Sucess": "User created!"}
    else:
        response = {"Error": "Invalid method"}
    return JsonResponse(response)

def signin(request):
    if request.method == "POST":
        login_information = json.loads(request.body.decode('UTF-8'))
        email = login_information["email"]
        password = login_information["password"]
        user = User.objects.get(email=email)
        if user and user.password == password:
            response = {"Sucess": "Login sucessfully"}
        else:
            response = {"Error": "Invalid e-mail or password"}
    else:
        response = {"Error": "Invalid method"}
    return JsonResponse(response)


def me(request):
    pass

