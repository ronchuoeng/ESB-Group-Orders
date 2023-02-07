from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

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
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "esb/login.html",
                {"message": "Invalid username and/or password."},
            )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
