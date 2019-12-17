from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from datetime import date

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class Validator(models.Manager):
    def registerValidator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "Name should be at least 2 characters"
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Your email must be in a valid format"
        if User.objects.filter(email=postData['email']):
            errors["emaildupe"] = "Your email is already registered"
        if postData["password"] != postData["c_password"]:
            errors["passwordmatch"] = "Your passwords don't match dawg"
        return errors

    def loginValidator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Your email must be in a valid format"
        user = User.objects.filter(email=postData['email'])
        if not user:
            errors["loginemail"] = "Email does not exist in Database"
            return errors
        else:
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                pass
            else:
                errors['password'] = "Your credentials do not match"
        return errors

    def fighterValidator(self, postData):
        errors = {}
        if len(postData['fightername']) < 1:
            errors["fightername"] = "Name should be at least 1 character"
        if len(postData['fighterdesc']) < 5:
            errors["fighterdesc"] = "Description should be at least 5 characters"
        return errors

    def editValidator(self,postData):
        errors = {}
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias should be at least 2 characters"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    desc = models.TextField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= Validator()

class Fighter(models.Model):
    fightername = models.CharField(max_length=255)
    fighterdesc = models.TextField()
    votes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="fighters", on_delete=models.CASCADE)
    objects= Validator()