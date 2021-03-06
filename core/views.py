import json

import jwcrypto.jwk as jwk
import python_jwt as jwt
from jwcrypto.jws import InvalidJWSObject
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User, Phone
from .utils import generateToken
from .schemas import signin_schema, signup_schema
from jsonschema import validate, ValidationError

#The csrf token authentication is disabled to allow testing using Postman
@csrf_exempt
def signup(request):
    #This view only accepts POST requests
    if request.method == "POST":
        user_json = json.loads(request.body.decode('UTF-8'))
        try:
            #Validate to check if all fields in body are right
            validate(user_json, schema=signup_schema)

            #Check if the email already exists on database
            if User.objects.filter(email=user_json["email"]).count() > 0:
                response = {"message": "E-mail already exists", "errorCode": 1}
            else:
                #Register the user and his phones
                new_user = User(
                    firstName = user_json["firstName"],
                    lastName = user_json["lastName"],
                    email = user_json["email"],
                    password = user_json["password"]
                )
                new_user.save()

                for phone in user_json["phones"]:

                    new_phone = Phone(
                        ownerEmail = user_json["email"],
                        number = phone["number"],
                        area_code = phone["area_code"],
                        country_code = phone["country_code"]
                    )
                    new_phone.save()
                #If the key for this session hasn't been generated, do it. This key will
                #be used to generate and verify jwts while this session is active
                if "key_json" not in request.session:
                    request.session["key_json"] = jwk.JWK.generate(kty='oct', size=256).export()
                
                #Generate the JWT token using the key, and give it as response
                key = jwk.JWK.from_json(request.session["key_json"])
                token = generateToken(new_user.email, new_user.password, key)
                response = {"token": token}
        except ValidationError as err:
            response = {"message": "Validation error", "errorCode": 2}
    else:
        response = {"message": "Invalid method", "errorCode": 3}
    return JsonResponse(response)

@csrf_exempt
def signin(request):

    if request.method == "POST":
        #This view only accepts POST requests
        try:
            #Validate to check if all fields in body are right
            login_information = json.loads(request.body.decode('UTF-8'))
            validate(login_information, signin_schema)

            #Check if the email and password are corrects
            email = login_information["email"]
            password = login_information["password"]
            user = User.objects.filter(email=email)
            if user.count() == 1 and user.first().password == password:
                #if yes, generate a JWT token using the key and give it 
                # as response for the request.
                if "key_json" not in request.session:
                    request.session["key_json"] = jwk.JWK.generate(kty='oct', size=256).export()
                key = jwk.JWK.from_json(request.session["key_json"])
                token = generateToken(email, password, key)
                response = {"token": token}
            else:
                response = {"message": "Invalid e-mail or password", "errorCode": 4}
        except ValidationError as err:
            response = {"message": "Validation error", "errorCode": 2}
    else:
        response = {"message": "Invalid method", "errorCode": 3}
    return JsonResponse(response)

@csrf_exempt
def me(request):
    if request.method == "GET":
        #This endpoint only accept GET requests
        #The request only will be processed if the header "Authorization" 
        # is in the request.  
        if 'Authorization' in request.headers:
            
            token = request.headers['Authorization']
            if "key_json" not in request.session:
                    request.session["key_json"] = jwk.JWK.generate(kty='oct', size=256).export()
            #Using the key, the JWT token is verified
            key = jwk.JWK.from_json(request.session["key_json"])
            try:
                data = jwt.verify_jwt(token, key, ['HS256'])[1]
                email = data["email"]
                #Using the email recovered from JWT, the data from this
                # specific user is searched and given as response
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
                response = {"message": "Unauthorized - invalid session", "errorCode": 5}
            except InvalidJWSObject:
                response = {"message": "Invalid JWT", "errorCode": 6}    
        else:
            response = {"message": "Unauthorized", "errorCode": 7}    
    else:
        response = {"message": "Invalid method", "errorCode": 3}
    return JsonResponse(response)

