import sqlite3

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

# def index(request):
#     return render(request, "pizza/authenticate.html")

def index(request):
    if not request.user.is_authenticated:
        return render(request, "pizza/authenticate.html", {"message": ""})
    context = {
        "user": request.user
    }
    return render(request, "pizza/index.html", context=context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "pizza/authenticate.html", {"message": "Invalid Credentials"})

def signup_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    # CREATE USER
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
    except sqlite3.IntegrityError:
        return render(request, "pizza/authenticate.html", {"message": "Account Already Created"})
    # LOGIN USER
    login(request, user)
    return HttpResponseRedirect(reverse("index"))


def logout_view(request):
    logout(request)
    return render(request, "pizza/authenticate.html", {"message": "Logged Out"})
