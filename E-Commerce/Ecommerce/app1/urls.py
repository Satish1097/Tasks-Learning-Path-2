from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("registeration", views.registeration, name="registeration"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("shopping", views.shopping, name="shopping"),
    path("blog", views.blog, name="blog"),
    path("contact", views.contact, name="contact"),
    path("shop_detail<int:product_id>", views.shop_detail, name="shop_detail"),
    path("shoping_cart", views.shoping_cart, name="shoping_cart"),
    path("add_to_cart<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path(
        "remove_from_cart<int:product_id>",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path(
        "add_to_wishlist/<int:product_id>",
        views.add_to_wishlist,
        name="add_to_wishlist",
    ),
    path("checkout", views.checkout, name="checkout"),
    path("blog_details", views.blog_details, name="blog_details"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("filter_products", views.filter_products, name="filter_products"),
]
