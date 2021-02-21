from django.shortcuts import render
import json

from middlewares.requests import post_request
from users.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import bcrypt
import base64
import hashlib
from .authtoken import *
from .models import AuthToken

# Create your views here.
@csrf_exempt
@post_request
def login(request, *args, **kwargs):
    body = json.loads(request.body)
    user = User.objects.filter(username=body["username"]).first()
    if bcrypt.checkpw(body["password"].encode(), user.password.encode()):
        authtoken = AuthToken()
        authtoken.user = user
        authtoken.token = generate_token()
        authtoken.save()
        return JsonResponse({
            'message': f"Welcome User {user.username}",
            'token': authtoken.token,
        })
    else:
        return JsonResponse({
            "message": f"Invalid Login Credentials!"
        })
    
@csrf_exempt
@post_request
def register(request, *args, **kwargs):
    body = json.loads(request.body)
    user = User()
    user.first_name = body["first_name"]
    user.last_name = body["last_name"]
    user.username = body["username"]
    user.email = body["email"]
    user.password = bcrypt.hashpw(
        body["password"].encode(),
        bcrypt.gensalt(),
        ).decode()
    user.enabled = True

    user.save()

    return JsonResponse({ "msg": "User saved Successfully" })