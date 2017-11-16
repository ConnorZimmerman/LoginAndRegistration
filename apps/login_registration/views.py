# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'login_registration/index.html')

def LoginValidator(request):
    response = User.objects.login_validator(request.POST)
    #print response["user"]
    print response["errors"]
    if response["status"] == False:
        for val in response["errors"]:
            messages.error(request, val, extra_tags="Login")
        return redirect('/')
    else:
        request.session["login"] = "Successfully logged in!!"
        request.session["user"] = response["user"].id
        return redirect('/success')

def RegistrationValidator(request):
    response = User.objects.registration_validator(request.POST)
    if response["status"] == False:
        for val in response["errors"]:
            messages.error(request, val, extra_tags="Registration")
        return redirect('/')
    else:
        request.session["login"] = "Successfully registered!"
        request.session["user"] = response["user"].id
        return redirect('/success')

def Success(request):
    if "user" not in request.session:
        return redirect('/')
    context = {
        "sessionUser" : User.objects.get(id = request.session["user"])
        }
    return render(request, 'login_registration/success.html', context)

def logOut(request):
    request.session.clear()
    return redirect('/')
