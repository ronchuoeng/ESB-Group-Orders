from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import IntegrityError
from django import forms
from django.contrib.admin.widgets import (
    AdminSplitDateTime,
    AdminDateWidget,
    AdminTimeWidget,
)
from .models import Purchases, User

# Create your views here.


def index(request):
    return render(request, "esb/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is None:
            return render(
                request,
                "esb/login.html",
                {"message": "Invalid username and/or password."},
            )
        else:
            if user.email_is_verified:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(
                    request,
                    "esb/login.html",
                    {
                        "messages": "You need to activate your account by verifying your email first."
                    },
                )
    else:
        return render(request, "esb/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        # Ensure password matches confirmation
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(
                request, "esb/register.html", {"messages": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "esb/register.html", {"messages": "Username already taken."}
            )
        return HttpResponse(
            "Account has been successfully created.<a href='www.google.com'>www.google.com</a>"
        )
    else:
        return render(request, "esb/register.html")
