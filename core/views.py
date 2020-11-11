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

@csrf_exempt
def signin(request):
    if request.method == "POST":
        login_information = json.loads(request.body.decode('UTF-8'))
        email = login_information["email"]
        password = login_information["password"]
        user = User.objects.filter(email=email)
        if user.count() == 1 and user.first().password == password:
            response = {"Sucess": "Login sucessfully"}
        else:
            response = {"Error": "Invalid e-mail or password"}
    else:
        response = {"Error": "Invalid method"}
    return JsonResponse(response)

@csrf_exempt
def me(request):
    if request.method == "GET":
        user = User.objects.get(email=email)
        phones = Phone.objects.get(ownerEmail=email)
        response = {
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "phones": []
        }
        for phone in phones:
            phone_json = {
                "number": phone["number"],
                "area_code": phone["area_code"],
                "country_code": phone["country_code"]
            }
            response["phones"].append(phone_json)
    else:
        response = {"Error": "Invalid method"}
    return JsonResponse(response)

