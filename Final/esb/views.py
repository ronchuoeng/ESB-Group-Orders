import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Q
from django import forms
from django.contrib.admin.widgets import (
    AdminSplitDateTime,
    AdminDateWidget,
    AdminTimeWidget,
)
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Product, PurchaseOrder, User, Customer, Category, CustomerPurchase
from .utils import send_email_token
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import uuid

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
                {"messages": "Invalid username and/or password."},
            )
        else:
            if user.email_is_verified:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                send_email_token(user.email, user.email_token)
                return render(
                    request,
                    "esb/login.html", {
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
                request, "esb/register.html", {
                    "messages": "Passwords must match."
                })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.email_token = str(uuid.uuid4())
            user.save()
            send_email_token(email, user.email_token)
        except IntegrityError:
            return render(
                request, "esb/register.html", {
                    "messages": "Username already taken."}
            )
        return HttpResponse(
            "Account has been successfully created.<a href='login'> Back to login page.</a>"
        )
    else:
        return render(request, "esb/register.html")


def verify(request, token):
    try:
        user = User.objects.get(email_token=token)
        user.email_is_verified = True
        user.save()
        return HttpResponse("Your account verified.")
    except Exception as e:
        return HttpResponse("Verify token is invalid/expired.")


@login_required
def settings_view(request):
    user = User.objects.get(username=request.user.username)
    return render(request, "esb/settings.html", {"user": user})


@csrf_exempt
def edit_settings(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username", "")
        phone = data.get("phone", "")
        address = data.get("address", "")

        user = User.objects.get(username=request.user.username)

        # Create Customer model of user
        try:
            customer = Customer.objects.create(
                user=user, name=username, phone=phone, address=address
            )
            return JsonResponse(
                {"message": "Account information successfully changed."}, status=201
            )
        except IntegrityError:
            customer = Customer.objects.get(user=user)
            customer.name = username
            customer.phone = phone
            customer.address = address
            customer.save()
            return JsonResponse(
                {"message": "Account information successfully changed."}, status=200
            )
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def category(request):
    # Get unique type of Category
    types = Category.objects.order_by(
        "type").values_list("type", flat=True).distinct()
    categories = {}
    for type in types:
        categories[type] = Category.objects.filter(type=type)

    return render(
        request,
        "esb/category.html",
        {"categories": categories, "types": types},
    )


def product_page(request):
    pass


def pending_page(request):
    # Get Orders that havent reached target & havent expired
    p_order = PurchaseOrder.objects.filter(date_time__gt=timezone.now())
    pendings = [order for order in p_order if not order.reach_target]
    # 18 items per page
    paginator = Paginator(pendings, 18)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Prev two pages
    prev_prev_page_number = page_obj.number - 2
    # Next two pages
    if page_obj.number + 2 in page_obj.paginator.page_range:
        next_next_page_number = page_obj.number + 2
    else:
        next_next_page_number = None

    return render(
        request,
        "esb/pendings.html",
        {
            "page_obj": page_obj,
            "next_next_page_number": next_next_page_number,
            "prev_prev_page_number": prev_prev_page_number,
        },
    )


def inprogress_page(request):
    # Get Orders that reached target & havent expired
    p_order = PurchaseOrder.objects.filter(date_time__gt=timezone.now())
    in_progress = [order for order in p_order if order.reach_target]
    # 18 items per page
    paginator = Paginator(in_progress, 18)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Prev two pages
    prev_prev_page_number = page_obj.number - 2
    # Next two pages
    if page_obj.number + 2 in page_obj.paginator.page_range:
        next_next_page_number = page_obj.number + 2
    else:
        next_next_page_number = None

    return render(
        request,
        "esb/inprogress.html",
        {
            "page_obj": page_obj,
            "next_next_page_number": next_next_page_number,
            "prev_prev_page_number": prev_prev_page_number,
        },
    )


def order_page(request, order_id):
    # Get Order model
    try:
        p_order = PurchaseOrder.objects.get(pk=order_id)
    except PurchaseOrder.DoesNotExist:
        return HttpResponse("This Purchase Order is invalid.")
    # Get User model
    user = User.objects.get(username=request.user.username)

    # Join/Edit order
    if request.method == "POST":
        # Get Customer model
        try:
            cus = Customer.objects.get(user=user)
        # If Customer model haven't create
        except Customer.DoesNotExist:
            return render(request, "esb/settings.html", {
                "user": user
            })
        quantity = request.POST.get('join')
        try:
            cusP = CustomerPurchase.objects.get(customer=cus, purchase=p_order)
            cusP.quantity = quantity
            cusP.save()
        except CustomerPurchase.DoesNotExist:
            cusP = CustomerPurchase.objects.create(
                customer=cus, purchase=p_order, quantity=quantity)

        return redirect("order_page", order_id)

    if request.method == "GET":
        # Get user in Customer model as customer
        customer = Customer.objects.get(user=user)
        # Check customer in order or not
        cus_in_order = p_order.customer_purchases.filter(
            customer=customer).exists()
        # Quantity of customer order
        cus_order_quantity = p_order.customer_purchases.get(
            customer=customer).quantity

        return render(request, "esb/order.html", {
            "p_order": p_order,
            "cus_in_order": cus_in_order,
            "cus_order_quantity": cus_order_quantity
        })


def refresh_order(request, order_id):
    if request.method == "GET":
        try:
            p_order = PurchaseOrder.objects.get(pk=order_id)
        except PurchaseOrder.DoesNotExist:
            return JsonResponse({"error": "This order is expired/not exist."}, status=404)
        target_quantity = p_order.target_quantity
        total_quantity = p_order.total_quantity
        return JsonResponse({"target_quantity": target_quantity, "total_quantity": total_quantity}, status=200)


def search_products(request):

    # search result split by blank space
    search = request.GET.get('q')
    if search:
        query = search.split()
        queries = [Q(title__icontains=q) for q in query]
        q_obj = queries.pop()
        for q in queries:
            q_obj |= q
        results = Product.objects.filter(q_obj)

        return render(request, "esb/search.html", {
            "query": query,
            "results": results
        })
    # default page
    else:
        return render(request, "esb/search.html")
