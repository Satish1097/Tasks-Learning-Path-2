from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("registeration", views.registeration, name="registeration"),
    path("createwallet", views.createwallet, name="createwallet"),
    path("addwallet", views.addwallet, name="addwallet"),
    path("add_amount", views.add_amount, name="add_amount"),
    path("paymenthandler", views.paymenthandler, name="paymenthandler"),
    path("transactionlist", views.transactionlist, name="transactionlist"),
    path("paymerchant", views.paymerchant, name="paymerchant"),
]
