from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
from app1.forms import registerationForm
from django.contrib import auth
from django.contrib.auth import authenticate
from django.db.models import F, Q
from django.db import transaction


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
        elif form.is_valid():
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
    categories = ProductCategory.objects.all()
    productspagination = Product.objects.all().order_by("-added_on")
    paginator = Paginator(productspagination, 10)
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
    products = Product.objects.all().order_by("-added_on")
    paginator = Paginator(products, 9)
    page_number = request.GET.get("page")
    allproducts = paginator.get_page(page_number)
    return render(request, "shop-grid.html", {"allproducts": allproducts})


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
        customer = Customer.objects.get(customer=user)
        cart = Cart.objects.get(owner=customer)
        cart_items = CartItem.objects.annotate(
            product_amount=F("product__price") * F("quantity")
        ).filter(cart=cart)

        for i in cart_items:
            cart_amount += i.product_amount
            print(i.product.stock)
        print(cart_amount)
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
        customer = Customer.objects.get(customer=request.user)
        cart = Cart.objects.get(owner=customer)
        try:
            cart_product = CartItem.objects.get(product=product)
            if cart_product is not None:
                messages.error(request, "Product already in cart")
                return redirect("shoping_cart")
        except CartItem.DoesNotExist:
            CartItem.objects.create(cart=cart, product=product)
            messages.success(request, "product added into cart")
            return redirect("shoping_cart")
    else:
        return redirect("login")


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        customer = Customer.objects.get(customer=request.user)
        cart = Cart.objects.get(owner=customer)
        cart_product = CartItem.objects.get(product=product, cart=cart)
        print(cart_product)
        cart_product.delete()
        messages.error(request, "Product deleted from cart")
        return redirect("shoping_cart")
    else:
        return redirect("login")


# def remove_from_cart(request, cart_item_id):
#     return redirect("cart")


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
        customer = Customer.objects.get(customer=user)
        cart = Cart.objects.get(owner=customer)
        cart_items = CartItem.objects.annotate(
            product_amount=F("product__price") * F("quantity")
        ).filter(cart=cart)
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
    user=request.user
    if user.is_authenticated:
        


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
