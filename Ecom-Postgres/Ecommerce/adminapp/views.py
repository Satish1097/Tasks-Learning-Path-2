from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from app1.models import *
from django.db.models import Sum
from django.db.models.functions import Lower
import datetime
from django.core.paginator import Paginator


def dashboard(request):
    user = request.user
    if user.is_superuser:
        allusers = User.objects.all()
        paginator = Paginator(allusers, 5)
        page_num = request.GET.get("pagenum")
        users = paginator.get_page(page_num)
        allorders = Order.objects.prefetch_related("order_item")
        paginator = Paginator(allorders, 5)
        page_number = request.GET.get("page")
        orders = paginator.get_page(page_number)

        total_price = sum(allorders.values_list("order_amount", flat=True))
        today_order = allorders.filter(created_on__gte=datetime.date.today())
        time = datetime.datetime.now() - datetime.timedelta(days=30)
        last_month_order = allorders.filter(created_on__gte=time)
        last_month_sale = sum(last_month_order.values_list("order_amount", flat=True))

        today_sale = sum(today_order.values_list("order_amount", flat=True))
        print(today_sale)
        print(total_price)
        print(last_month_sale)
        products = Product.objects.all()
        context = {
            "users": users,
            "orders": orders,
            "products": products,
            "total_price": total_price,
            "today_sale": today_sale,
            "last_month_sale": last_month_sale,
            "allorders": allorders,
        }
        return render(request, "dashboard.html", context)
    messages.error(request, "You are not authorized to perform this action")
    return redirect("/")


def userlists(request):
    user = request.user
    if user.is_superuser:
        users = User.objects.all().order_by(Lower("username"))
        return render(request, "userlist.html", {"users": users})
    messages.error(request, "You are not authorized to perform this action")
    return redirect("/")


def orderlists(request):
    user = request.user
    if user.is_superuser:
        orders = Order.objects.prefetch_related("order_item")
        return render(request, "orderlist.html", {"orders": orders})
    messages.error(request, "You are not authorized to perform this action")
    return redirect("/")


def itemlists(request):
    user = request.user
    if user.is_superuser:
        items = Product.objects.all()
        return render(request, "items.html", {"items": items})
    messages.error(request, "You are not authorized to perform this action")
    return redirect("/")
