import json

import jwcrypto.jwk as jwk
import python_jwt as jwt
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User, Phone
from .utils import generateToken

# Create your views here.
@csrf_exempt
def signup(request):

    if request.method == "POST":
        user_json = json.loads(request.body.decode('UTF-8'))
        if User.objects.filter(email=user_json["email"]).count() > 0:
            response = {"Error": "E-mail already exists"}
        else:
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

            if "key_json" not in request.session:
                request.session["key_json"] = jwk.JWK.generate(kty='oct', size=256).export()
            
            key = jwk.JWK.from_json(request.session["key_json"])
            token = generateToken(new_user.email, new_user.password, key)
            response = {"token": token}
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
            key = jwk.JWK.from_json(request.session["key_json"])
            token = generateToken(new_user.email, new_user.password, key)
            response = {"token": token}
        else:
            response = {"Error": "Invalid e-mail or password"}
    else:
        response = {"Error": "Invalid method"}
    return JsonResponse(response)

@csrf_exempt
def me(request):
    if request.method == "GET":
        if 'Authorization' in request.headers:
            
            token = request.headers['Authorization']
            key = jwk.JWK.from_json(request.session["key_json"])
            try:
                data = jwt.verify_jwt(token, key, ['HS256'])[1]
                email = data["email"]
                
                user = User.objects.get(email=email)
                phones = Phone.objects.filter(ownerEmail=email)
                response = {
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phones": []
                }
                for phone in phones:
                    phone_json = {
                        "number": phone.number,
                        "area_code": phone.area_code,
                        "country_code": phone.country_code
                    }
                    response["phones"].append(phone_json)
            except jwt._JWTError:
                response = {"Error": "Unauthorized - invalid session"}    
        else:
            response = {"Error": "Unauthorized"}    
    else:
        response = {"Error": "Invalid method"}
    return JsonResponse(response)

