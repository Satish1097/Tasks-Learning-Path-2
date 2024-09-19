from django.shortcuts import (
    render,
    redirect,
    HttpResponse,
    get_object_or_404,
)
from django.http import JsonResponse
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
from app1.forms import registerationForm
from django.contrib import auth
from django.contrib.auth import authenticate
from django.db.models import F, Q
from django.db.models.functions import Round
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.db.models import FloatField

# import razorpay
import stripe
from django.conf import settings
from django.urls import reverse


def newcheckout(request):
    user = request.user
    if user.is_authenticated:
        total_amount = 0
        cart_items = CartItem.objects.annotate(
            product_amount=F("product__price") * F("quantity")
        ).filter(user=user)
        for i in cart_items:
            if i.product.stock > 0:
                total_amount += i.product_amount
    return render(
        request,
        "checkout.html",
        {"cart_items": cart_items, "total_amount": total_amount},
    )


@transaction.atomic
def orderproducts(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            FirstName = request.POST.get("firstname")
            LastName = request.POST.get("lastname")
            Address = request.POST.get("address")
            Country = request.POST.get("country")
            State = request.POST.get("state")
            City = request.POST.get("city")
            PinCode = request.POST.get("pincode")
            Email = request.POST.get("email")
            Phone = request.POST.get("phone")
            if (
                FirstName == ""
                or LastName == ""
                or Address == ""
                or Country == ""
                or State == ""
                or City == ""
                or PinCode == ""
                or Email == ""
                or Phone == ""
            ):
                messages.error(request, "All fields are required")
                return redirect("checkout")

            with transaction.atomic():
                cart_items = CartItem.objects.annotate(
                    product_amount=F("product__price") * F("quantity")
                ).filter(user=user)

                amount_to_pay = 0
                in_stock_items = []
                out_of_stock_items = []
                items = []
                for item in cart_items:
                    product = Product.objects.select_for_update().get(
                        id=item.product.id
                    )
                    if product.stock < item.quantity:
                        out_of_stock_items.append(product)
                    else:
                        in_stock_items.append((product, item.quantity))
                        amount_to_pay += item.product_amount
                    if amount_to_pay == 0:
                        messages.error(request, "Product not in cart or out of stock")
                        return redirect("shoping_cart")
                order = Order.objects.create(user=user, order_amount=amount_to_pay)
                billing_address = Billing_Address.objects.create(
                    order=order,
                    FirstName=FirstName,
                    LastName=LastName,
                    Country=Country,
                    State=State,
                    Address=Address,
                    City=City,
                    PinCode=PinCode,
                    Email=Email,
                    phone=Phone,
                )
                billing_address.save()
                for product, quantity in in_stock_items:
                    order_item = OrderItem.objects.create(
                        order=order, product=product, quantity=quantity
                    )
                    obj = {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": order_item.order.orderid,
                                "images": [
                                    "http://127.0.0.1:8000"
                                    + "/images/meadia/"
                                    + str(product.image)
                                ],
                            },
                            "unit_amount": int(product.price * 100),
                        },
                        "quantity": order_item.quantity,
                    }
                    items.append(obj)

                    # product.stock -= quantity
                    # product.save()
                    CartItem.objects.get(product=product, user=user).delete()
                stripe.api_key = settings.STRIPE_SECRET_KEY
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=items,
                    mode="payment",
                    success_url=request.build_absolute_uri(reverse("success")),
                    cancel_url=request.build_absolute_uri(reverse("cancel")),
                )
            return redirect(checkout_session.url)
    else:
        return redirect("login")


stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = (
        "whsec_4e5befdba119393bd0c8f3562ac289a9e1d01ac7d9d60c96f100ebd91e14e125"
    )
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session_id)
        order_id = []
        amount = session["amount_total"]
        print(amount)
        for item in line_items.data:
            print("Item:", item.description)
            order_id = item.description
        print(f"order_id", order_id)
        stock_cart_management(order_id, amount)
        print("Payment was successful.")
    if event["type"] == "payment_intent.succeeded":
        print("payment done")
    return HttpResponse(status=200)


def stock_cart_management(order_id, amount):
    order_items = OrderItem.objects.filter(order=order_id)
    with transaction.atomic():
        for i in order_items:
            i.product.stock -= i.quantity
            i.product.save()

    order = Order.objects.get(orderid=order_id)
    order.payment_status = True
    order.save()
    transactiondetail = TransactionDetail.objects.create(
        order_id=order, amount=amount / 100, payment_status=True
    )


def registeration(request):
    if request.method == "POST":
        form = registerationForm(request.POST)
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if (
            firstname == ""
            or lastname == ""
            or username == ""
            or email == ""
            or password == ""
        ):
            messages.error(request, "all fields are required")
        elif len(username) < 5:
            messages.error(request, "username must have 5 charater or more")
        elif len(password) < 8:
            messages.error(request, "password must have 8 digit or more")
        elif password == username:
            messages.error(request, "password should not same as  username")
        elif password == firstname:
            messages.error(request, "password should not same as  firstname")
        elif password == lastname:
            messages.error(request, "password should not same as  lastname")
        else:
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Registered")
                return redirect("login")
            else:
                messages.error(request, "invalid form data")
                return redirect("registeration")
    else:
        form = registerationForm()
    return render(request, "registeration.html", {"form": form})


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            messages.success(request, "Login Successfully")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credential")
            return redirect("../login")
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/login")


def home(request):
    user = request.user
    sale_id = []
    product_in_sale = Product_in_sale.objects.all()
    for i in product_in_sale:
        sale_id.append(i.product.id)
    print(sale_id)
    categories = ProductCategory.objects.all()
    productspagination = Product.objects.exclude(id__in=sale_id).order_by("-added_on")
    paginator = Paginator(productspagination, 8)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)
    blogs = Blogpost.objects.all().order_by("-created_on")[0:3]
    top_rated_product = Product.objects.all().order_by("-stock")
    context = {
        "categories": categories,
        "products": products,
        "blogs": blogs,
        "top_rated_product": top_rated_product,
    }
    return render(request, "index.html", context)


def shopping(request):
    sale_id = []
    product_in_sale = Product_in_sale.objects.annotate(
        discount=Round(
            (F("product__price") - F("discounted_price")) * 100 / F("product__price"), 1
        )
    )
    for i in product_in_sale:
        sale_id.append(i.product.id)
    products = Product.objects.exclude(id__in=sale_id).order_by("-added_on")
    paginator = Paginator(products, 9)
    page_number = request.GET.get("page")
    allproducts = paginator.get_page(page_number)
    return render(
        request,
        "shop-grid.html",
        {"allproducts": allproducts, "product_in_sale": product_in_sale},
    )


def blog(request):
    blogs = Blogpost.objects.all().order_by("-created_on")
    paginator = Paginator(blogs, 4)
    page_number = request.GET.get("page")
    allblogs = paginator.get_page(page_number)
    return render(request, "blog.html", {"allblogs": allblogs})


def contact(request):
    return render(request, "contact.html")


def shop_detail(request, product_id):
    user = request.user
    if user.is_authenticated:
        product = Product.objects.get(id=product_id)
        related_product = Product.objects.filter(category=product.category)
        # reviewed = Reviewed_product.objects.get(user=user)
        # reviewed.product.add(product)
        return render(
            request,
            "shop-details.html",
            {"product": product, "related_product": related_product},
        )
    else:
        return redirect("login")


def shoping_cart(request):
    user = request.user
    if user.is_authenticated:
        cart_amount = 0
        cart_items = CartItem.objects.annotate(
            product_amount=F("product__price") * F("quantity")
        ).filter(user=user)

        for i in cart_items:
            cart_amount += i.product_amount
        return render(
            request,
            "shoping-cart.html",
            {
                "cart_items": cart_items,
                "cart_amount": cart_amount,
            },
        )
    else:
        return redirect("login")


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        try:
            cart_product = CartItem.objects.get(product=product, user=request.user)
            if cart_product is not None:
                messages.error(request, "Product already in cart")
                return redirect("shoping_cart")
        except CartItem.DoesNotExist:
            CartItem.objects.create(user=request.user, product=product)
            messages.success(request, "product added into cart")
            return redirect("shoping_cart")
    else:
        return redirect("login")


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart_product = CartItem.objects.get(product=product, user=request.user)
        cart_product.delete()
        messages.error(request, "Product deleted from cart")
        return redirect("shoping_cart")
    else:
        return redirect("login")


def add_to_wishlist(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        customer = Customer.objects.get(customer=request.user)
        wishlist = Wishlist.objects.get(customer=customer)
        wishlist.product.add(product)
        messages.success(request, "product added into wishlist")
        return redirect("home")
    else:
        return redirect("login")


def checkout(request):
    user = request.user
    if user.is_authenticated:
        total_amount = 0
        cart_items = CartItem.objects.annotate(
            product_amount=F("product__price") * F("quantity")
        ).filter(user=user)
        for i in cart_items:
            if i.product.stock > 0:
                total_amount += i.product_amount
        return render(
            request,
            "checkout.html",
            {"cart_items": cart_items, "total_amount": total_amount},
        )
    else:
        return redirect("login")


def blog_details(request):
    return render(request, "blog-details.html")


def wishlist(request):
    user = request.user
    if user.is_authenticated:
        customer = Customer.objects.get(customer=user)
        wishlists = Wishlist.objects.get(customer=customer)

        return render(request, "wishlist.html", {"wishlists": wishlists})
    else:
        return redirect("login")


def filter_products(request):
    query = request.GET.get("query")

    products = Product.objects.filter(
        Q(name__icontains=query) | Q(category__categoryname__icontains=query)
    )

    return render(request, "product_list.html", {"products": products, "query": query})


def filter_products_by(request, category):
    query = category

    products = Product.objects.filter(category__categoryname__icontains=query)

    return render(request, "product_list.html", {"products": products, "query": query})


def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")


def add_to_cart_detail(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        quantity = request.POST.get("quantity")
        try:
            cart_product = CartItem.objects.get(product=product, user=request.user)
            if cart_product is not None:
                messages.error(request, "Product already in cart")
                return redirect("shoping_cart")
        except CartItem.DoesNotExist:
            CartItem.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
            )
            messages.success(request, "product added into cart")
            return redirect("shoping_cart")
    else:
        return redirect("login")


def add_quantity(request, product_id):
    user = request.user
    if user.is_authenticated:
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(user=user, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return redirect("shoping_cart")
    return redirect("login")


def sub_quantity(request, product_id):
    user = request.user
    if user.is_authenticated:
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(user=user, product=product)
        if cart_item.quantity == 1:
            return redirect("shoping_cart")
        cart_item.quantity -= 1
        cart_item.save()
        return redirect("shoping_cart")
    return redirect("login")


def orderdetails(request):
    user = request.user
    if user.is_authenticated:
        # Fetch orders for a specific user with prefetch_related
        orders = (
            Order.objects.prefetch_related("order_item")
            .filter(user=user)
            .order_by("-created_on")
        )
        # # Iterate over each order
        # for order in orders:
        #     print(f"Order ID: {order.orderid}")
        #     # Access related order items for each order
        #     for item in order.order_item.all():
        #         print(f"  Product: {item.product}, Quantity: {item.quantity}")

        return render(request, "order.html", {"orders": orders})


def pay_again(request, order_id):
    order_items = OrderItem.objects.filter(order=order_id)
    items = []
    for item in order_items:
        obj = {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.order.orderid,
                    "images": [
                        "http://127.0.0.1:8000" + "/images/" + str(item.product.image)
                    ],
                    # "images": [
                    #     "https://satish1097.pythonanywhere.com/media/media/ST.jpg"
                    # ],
                },
                "unit_amount": int(item.product.price * 100),
            },
            "quantity": item.quantity,
        }
        items.append(obj)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=items,
        mode="payment",
        success_url=request.build_absolute_uri(reverse("success")),
        cancel_url=request.build_absolute_uri(reverse("cancel")),
    )
    return redirect(checkout_session.url)
    # return redirect("orderdetails")


# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import json


@csrf_exempt  # Allowing CSRF exemption for this view (not recommended for production)
@require_POST
def update_quantity(request):
    user = request.user
    data = json.loads(request.body)
    product_id = data.get("productId")
    new_quantity = data.get("newQuantity")
    print(product_id)

    try:
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(product=product, user=user)
        cart_item.quantity = new_quantity
        cart_item.save()
        return JsonResponse({"newQuantity": new_quantity})
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def testview(request):
    return render(request, "test.html")


def blogdetail(request, blog_id):
    blogpost = Blogpost.objects.get(id=blog_id)
    blogs = Blogpost.objects.all().order_by("-created_on")[0:3]
    return render(request, "blog-details.html", {"blogpost": blogpost, "blogs": blogs})
