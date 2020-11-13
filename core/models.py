from django.db import models

class User(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    

class Phone(models.Model):
    ownerEmail = models.EmailField(max_length=100)
    number = models.CharField(max_length=100)
    area_code = models.CharField(max_length=100)
    country_code = models.CharField(max_length=100)

