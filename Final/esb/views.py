from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseForbidden
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
from .models import Product, PurchaseOrder, User, Customer, Category, CustomerPurchase, ProductImage
from .utils import send_email_token
from django.utils import timezone
from datetime import timedelta, datetime
from django.views.decorators.csrf import csrf_exempt
import uuid
import json

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
            messages.warning(request, "Invalid username and/or password.")
            return render(
                request,
                "esb/login.html",
            )
        else:
            if user.email_is_verified:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                send_email_token(user.email, user.email_token)
                messages.error(
                    request, f"Please verify your email first: {user.email} ")
                return render(
                    request,
                    "esb/login.html"
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
                    "message": "Passwords must match."
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
                    "message": "Username already taken."}
            )
        messages.success(request, "Successfully created account.")
        return redirect('login')
    else:
        return render(request, "esb/register.html")


def verify(request, token):
    try:
        user = User.objects.get(email_token=token)
        user.email_is_verified = True
        user.save()
        messages.success(request, "Successfully verified account.")
        return redirect("login")
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


def category_products(request, category_name):
    category = Category.objects.get(title=category_name)
    products = Product.objects.filter(category=category)

    # Make Pagination
    # 18 items per page
    paginator = Paginator(products, 18)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Prev two pages
    prev_prev_page_number = page_obj.number - 2
    # Next two pages
    if page_obj.number + 2 in page_obj.paginator.page_range:
        next_next_page_number = page_obj.number + 2
    else:
        next_next_page_number = None

    return render(request, "esb/categoryP.html", {
        "category": category,
        "page_obj": page_obj,
        "next_next_page_number": next_next_page_number,
        "prev_prev_page_number": prev_prev_page_number
    })


def pending_page(request):
    # Get Orders that havent reached target & havent expired
    p_order = PurchaseOrder.objects.filter(date_time__gt=timezone.now())
    pendings = [order for order in p_order if not order.reach_target]

    # Make Pagination
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

    # Make Pagination
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

    # Join/Edit order
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.user.username)
        except:
            return redirect("login")
        # Get Customer model
        try:
            cus = Customer.objects.get(user=user)
        # If Customer model haven't create
        except Customer.DoesNotExist:
            return render(request, "esb/settings.html", {
                "user": user,
                "message": "Please complete your information before joining an order."
            })
        # form of quantity user submit
        quantity = request.POST.get('join')
        try:
            cusP = CustomerPurchase.objects.get(customer=cus, purchase=p_order)
            print(request.POST.get("action"))
            # If user click 'Join/Edit'
            if request.POST.get("action") == "join":
                cusP.quantity = quantity
                cusP.save()
            # If user click 'Cancel'
            elif request.POST.get("action") == "delete":
                cusP.delete()
        except CustomerPurchase.DoesNotExist:
            cusP = CustomerPurchase.objects.create(
                customer=cus, purchase=p_order, quantity=quantity)

        return redirect("order_page", order_id)

    if request.method == "GET":
        # Get user in Customer model as customer
        try:
            user = User.objects.get(username=request.user.username)
            customer = Customer.objects.get(user=user)
        except (User.DoesNotExist, Customer.DoesNotExist):
            return render(request, "esb/order.html", {
                "p_order": p_order,
            })
        # Check customer in order or not
        cus_in_order = p_order.customer_purchases.filter(
            customer=customer).exists()
        # Quantity of customer order
        try:
            cus_order_quantity = p_order.customer_purchases.get(
                customer=customer).quantity
        except CustomerPurchase.DoesNotExist:
            cus_order_quantity = 0

        return render(request, "esb/order.html", {
            "p_order": p_order,
            "cus_in_order": cus_in_order,
            "cus_order_quantity": cus_order_quantity
        })


def refresh_order(request, order_id):
    # refresh order page every 10 seconds(js file)
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
        # split the keyword with space
        query = search.split()
        queries = [Q(title__icontains=q) for q in query]
        q_obj = queries.pop()
        for q in queries:
            q_obj |= q
        results = Product.objects.filter(q_obj)

        # Make Pagination
        paginator = Paginator(results, 18)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # Prev two pages
        prev_prev_page_number = page_obj.number - 2
        # Next two pages
        if page_obj.number + 2 in page_obj.paginator.page_range:
            next_next_page_number = page_obj.number + 2
        else:
            next_next_page_number = None

        return render(request, "esb/search.html", {
            "query": query,
            "page_obj": page_obj,
            "results": results,
            "next_next_page_number": next_next_page_number,
            "prev_prev_page_number": prev_prev_page_number
        })
    # No Results
    else:
        return render(request, "esb/search.html")


def my_orders(request):
    # Get request user's Customer model and Customer Purchase model
    user = User.objects.get(username=request.user.username)
    try:
        # Customer model
        cus = Customer.objects.get(user=user)
        # CustomerPurchase model
        cusP = CustomerPurchase.objects.filter(
            customer=cus).order_by("-purchase_id")
    except (Customer.DoesNotExist, CustomerPurchase.DoesNotExist):
        # return myoders page with empty
        cusP = CustomerPurchase.objects.none()
        cus = None

    # Make Pagination
    paginator = Paginator(cusP, 18)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Prev two pages
    prev_prev_page_number = page_obj.number - 2
    # Next two pages
    if page_obj.number + 2 in page_obj.paginator.page_range:
        next_next_page_number = page_obj.number + 2
    else:
        next_next_page_number = None

    return render(request, "esb/myorders.html", {
        "page_obj": page_obj,
        "cusP": cusP,
        "next_next_page_number": next_next_page_number,
        "prev_prev_page_number": prev_prev_page_number
    })


def product(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return HttpResponse("The product does not exist.")
    try:
        join_order = product.order_product.get(
            date_time__gt=timezone.now())
    except PurchaseOrder.DoesNotExist:
        join_order = None

    return render(request, "esb/product.html", {
        "product": product,
        "join_order": join_order
    })


@login_required
def new_order(request, product_id):
    # Get the Product
    product = Product.objects.get(pk=product_id)
    # Get the Order of this product
    try:
        p_order = PurchaseOrder.objects.get(
            product=product, date_time__gt=timezone.now())
    # If not exists, create one
    except PurchaseOrder.DoesNotExist:
        date_time = timezone.now() + timedelta(weeks=2)
        p_order = PurchaseOrder.objects.create(
            product=product, date_time=date_time, target_quantity=100)

    return HttpResponseRedirect(reverse("order_page", args=(p_order.pk,)))


def manage_orders(request):
    if request.method == 'GET':
        p_orders = PurchaseOrder.objects.all().order_by('-date_time')

        # Make Pagination
        paginator = Paginator(p_orders, 14)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # Prev two pages
        prev_prev_page_number = page_obj.number - 2
        # Next two pages
        if page_obj.number + 2 in page_obj.paginator.page_range:
            next_next_page_number = page_obj.number + 2
        else:
            next_next_page_number = None

        return render(request, "esb/manage_orders.html", {
            "page_obj": page_obj,
            "next_next_page_number": next_next_page_number,
            "prev_prev_page_number": prev_prev_page_number
        })


def manage_products(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by("id")

        # Make pagination
        paginator = Paginator(products, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # Prev two pages
        prev_prev_page_number = page_obj.number - 2
        # Next two pages
        if page_obj.number + 2 in page_obj.paginator.page_range:
            next_next_page_number = page_obj.number + 2
        else:
            next_next_page_number = None

        return render(request, "esb/manage_products.html", {
            "page_obj": page_obj,
            "next_next_page_number": next_next_page_number,
            "prev_prev_page_number": prev_prev_page_number
        })


def order_details(request, order_id):
    p_order = PurchaseOrder.objects.get(pk=order_id)
    cus_in_order = CustomerPurchase.objects.filter(purchase=p_order)

    # Make Pagination
    paginator = Paginator(cus_in_order, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Prev two pages
    prev_prev_page_number = page_obj.number - 2
    # Next two pages
    if page_obj.number + 2 in page_obj.paginator.page_range:
        next_next_page_number = page_obj.number + 2
    else:
        next_next_page_number = None

    return render(request, "esb/order_details.html", {
        "page_obj": page_obj,
        "p_order": p_order,
        "next_next_page_number": next_next_page_number,
        "prev_prev_page_number": prev_prev_page_number
    })


@csrf_exempt
def delete_cus_order(request):
    # Staff required
    if request.user.is_staff:
        # Click Delete
        if request.method == 'DELETE':
            data = json.loads(request.body)
            cus_order_id = data.get("cus_order_id", "")
            cus_order = CustomerPurchase.objects.get(pk=cus_order_id)
            cus_order.delete()

            return JsonResponse({"message": "Successfully deleted."}, status=200)
        else:
            return JsonResponse({"error": "DELETE request required."}, status=400)
    else:
        return JsonResponse({"error": "Staff required."}, status=400)


@csrf_exempt
def save_edit_cus_order(request):
    # Staff required
    if request.user.is_staff:
        # Click Save
        if request.method == 'POST':
            data = json.loads(request.body)
            cus_order_id = data.get("cus_order_id", "")
            # edited quantity
            edited_cus_order_quantity = data.get(
                "edited_cus_order_quantity", "")
            cus_order = CustomerPurchase.objects.get(pk=cus_order_id)
            # Edit change
            cus_order.quantity = edited_cus_order_quantity
            # Save change
            cus_order.save()

            # Updated data (For refresh use)
            total_quantity = cus_order.purchase.total_quantity
            reach_target = cus_order.purchase.reach_target
            is_expired = cus_order.purchase.is_expired

            order_data = {"message": "Edited save successfully.",
                          "total_quantity": total_quantity,
                          "reach_target": reach_target,
                          "is_expired": is_expired}

            return JsonResponse(order_data, status=200)
        else:
            return JsonResponse({"error": "POST request required."}, status=400)

    else:
        return JsonResponse({"error": "Staff required."}, status=400)


@csrf_exempt
def delete_product(request):
    # Staff required
    if request.user.is_staff:
        # Click Delete
        if request.method == 'DELETE':
            data = json.loads(request.body)
            product_id = data.get('product_id', "")
            product = Product.objects.get(pk=product_id)
            p_order = PurchaseOrder.objects.filter(product=product)
            # Check if any ongoing orders related to the product
            if not p_order.exists():
                # If no, delete
                product.delete()
                return JsonResponse({"message": "Successfully deleted."}, status=200)
            else:
                # If there's order in progress
                all_orders_not_reached_target = True
                for order in p_order:
                    if order.reach_target:
                        all_orders_not_reached_target = False
                        break
                # If no order is in progress, delete
                if all_orders_not_reached_target:
                    product.delete()
                else:
                    return JsonResponse({"error": "There is at least an order in progress."}, status=400)
        else:
            return JsonResponse({"error": "DELETE request required."}, status=400)

    else:
        return JsonResponse({"error": "Staff requried."}, status=400)


@csrf_exempt
def delete_purchase_order(request):
    # Staff required:
    if request.user.is_staff:
        # Click Delete
        if request.method == 'DELETE':
            data = json.loads(request.body)
            p_order_id = data.get("p_order_id", "")
            p_order = PurchaseOrder.objects.get(pk=p_order_id)
            p_order.delete()

            return JsonResponse({"message": "Successfully deleted."}, status=200)
        else:
            return JsonResponse({"error": "DELETE request required."}, status=400)
    else:
        return JsonResponse({"error": "Staff required"}, status=400)


@csrf_exempt
def save_edit_p_order(request):
    # Staff required
    if request.user.is_staff:
        # Click Edit
        if request.method == 'POST':
            data = json.loads(request.body)
            p_order_id = data.get("p_order_id", "")
            # edited target quantity
            edited_target_quantity = int(
                data.get("edited_target_quantity", ""))
            edited_expiration_datetime_str = data.get(
                "edited_expiration_datetime", "")
            edited_expiration_datetime = datetime.fromisoformat(
                edited_expiration_datetime_str)
            # Get the Order
            p_order = PurchaseOrder.objects.get(pk=p_order_id)
            # Edit change
            p_order.target_quantity = edited_target_quantity
            p_order.date_time = edited_expiration_datetime
            # Save change
            p_order.save()

            # Updated data( For refresh use)
            target_quantity = p_order.target_quantity
            date_time = p_order.date_time
            reach_target = p_order.reach_target
            is_expired = p_order.is_expired

            p_order_data = {"message": "Succesfully edited.",
                            "target_quantity": target_quantity,
                            "date_time": date_time,
                            "reach_target": reach_target,
                            "is_expired": is_expired
                            }
            return JsonResponse(p_order_data, status=200)
        else:
            return JsonResponse({"error": "POST request required."}, status=400)
    else:
        return JsonResponse({"error": "Staff required."}, status=400)


@csrf_exempt
def create_product(request):
    if not request.user.is_staff:
        messages.warning(request, "You are not allowed to access this page.")
        return redirect('/')

    if request.method == "GET":
        try:
            product = Product.objects.get(
                title="title", description="description", price=0)
        except Product.DoesNotExist:
            product = Product.objects.create(
                title="title", description="description", price=0)
        # Get categories
        types = Category.objects.order_by(
            "type").values_list("type", flat=True).distinct()
        categories = {}
        for type in types:
            categories[type] = Category.objects.filter(type=type)

        return render(request, "esb/create_product.html", {
            "product": product,
            "categories": categories,
            "types": types
        })

    if request.method == "POST":
        product_id = request.POST.get("product-id")
        title = request.POST.get("title")
        price = request.POST.get("price")
        type_category = request.POST.get("type-category")
        title_category = request.POST.get("title-category")
        description = request.POST.get("description")
        # Get Product
        product = Product.objects.get(pk=product_id)
        # Get Category
        try:
            category = Category.objects.get(
                type=type_category, title=title_category)
        except Category.DoesNotExist:
            category = None
        # Fill the information of product
        product.title = title
        product.price = price
        product.category = category
        product.description = description
        product.save()
        return redirect('manage_products')


@csrf_exempt
def edit_product(request, product_id):
    if request.method == "GET":
        product = Product.objects.get(pk=product_id)
        return render(request, "esb/create_product.html", {
            "product": product
        })


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('images'):
        product_id = request.POST.get("product_id", "")
        image = request.FILES.get('images')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            product = Product.objects.create(
                title="title", description="description", price=0)
        product_image = ProductImage.objects.create(
            product=product, image=image)
        image_url = product_image.image.url
        return JsonResponse({'image_url': image_url, 'product_id': product_id}, status=201)
    return JsonResponse({'error': 'No image was uploaded.'}, status=400)


@csrf_exempt
def active_product(request, product_id):
    if not request.user.is_staff:
        messages.warning(request, "You are not allowed to access this page.")
        return redirect('/')

    if request.method == "PUT":
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            messages.warning("Product does not exist.")
            return redirect('manage_product')

        if product.active:
            product.active = False
        else:
            product.active = True
        product.save()
        return HttpResponse(status=204)


def update_sub_categories(request, type_select):
    if request.method == "GET":
        categories = Category.objects.filter(type=type_select).values()
        return JsonResponse({"categories": list(categories)}, status=200)
