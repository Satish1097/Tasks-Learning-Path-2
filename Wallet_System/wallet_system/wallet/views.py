from django.shortcuts import render, redirect, HttpResponse
from .forms import registerationForm, WalletForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate
from .models import *
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.core.mail import send_mail
from django.http import JsonResponse
from django.db import transaction
from django.utils.crypto import get_random_string


def home(request):
    return render(request, "index.html")


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
            # return redirect("profile")
        else:
            messages.error(request, "Invalid Credential")
            return redirect("../login")
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/login")


def createwallet(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            form = WalletForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                print(form)
                profile.user = user
                profile.save()
                return redirect("home")
        else:
            form = WalletForm()
        return render(request, "Wallet.html", {"form": form})
    return redirect("login")


def add_amount(request):
    user = request.user
    if user.is_authenticated:
        try:
            wallet = Wallet.objects.get(user=user)
            if wallet:
                if request.method == "POST":
                    x = request.POST.get("Wallet_amount")
                    if int(x) > 0 and int(x) < 100000:
                        amount = int(x)
                        currency = "INR"
                        client = razorpay.Client(
                            auth=("rzp_test_dAeKznpfJoVqVt", "OA8xXFOj9pRlxQq0SmHe5KEc")
                        )
                        payment = client.order.create(
                            dict(
                                amount=amount * 100,  # Amount in paise
                                currency=currency,
                                payment_capture="0",
                            )
                        )
                        razorpay_order_id = payment["id"]
                        callback_url = "paymenthandler"
                        context = {
                            "razorpay_order_id": razorpay_order_id,
                            "razorpay_merchant_key": settings.RAZOR_KEY_ID,
                            "razorpay_amount": amount,
                            "currency": currency,
                            "callback_url": callback_url,
                        }
                        return render(request, "addWallet.html", context=context)
                    else:
                        messages.error(request, "Enter Valid Amount")
                        return redirect("add_amount")
                else:
                    return render(request, "addamount.html")
            else:
                return redirect("createwallet")
        except Wallet.DoesNotExist:
            return redirect("createwallet")
    else:
        return redirect("login")


@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            # Print and handle the incoming POST data for debugging
            print(request.POST)

            # Initialize the Razorpay client with your API keys
            razorpay_client = razorpay.Client(
                auth=("rzp_test_dAeKznpfJoVqVt", "OA8xXFOj9pRlxQq0SmHe5KEc")
            )

            payment_id = request.POST.get("razorpay_payment_id", "")
            razorpay_order_id = request.POST.get("razorpay_order_id", "")
            signature = request.POST.get("razorpay_signature", "")
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }

            print(params_dict)
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:  # Payment signature verification successful
                order = razorpay_client.order.fetch(razorpay_order_id)
                amount = order["amount"]
                print(amount)
                try:
                    # Capture the payment
                    razorpay_client.payment.capture(payment_id, amount)

                    # Create a new Transaction_detail object for successful payment
                    create_transaction(
                        request.user,
                        amount / 100,
                        "credit",
                        "success",
                        "Wallet",
                        payment_id,
                    )

                    # Update the wallet balance
                    wallet = Wallet.objects.get(user=request.user)
                    wallet.Wallet_amount += amount / 100
                    wallet.save()

                    # Send payment success notification
                    send_mail(
                        subject="Payment Status",
                        message="Payment done Successfully",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[request.user.email],
                        fail_silently=True,
                    )
                    return render(request, "paymentsuccess.html")

                except Exception as e:  # Payment capture failed
                    # Create a new Transaction_detail object for failed payment
                    create_transaction(
                        request.user, amount / 100, "credit", "failed", "Wallet"
                    )
                    messages.error(request, f"Error capturing payment: {str(e)}")
                    return render(request, "paymentfail.html")
            else:
                # Signature verification failed
                create_transaction(
                    request.user,
                    amount / 100,
                    "credit",
                    "pending",
                    "Wallet",
                    payment_id,
                )
                messages.error(request, "Signature verification failed.")
                return render(request, "paymentfail.html")
        except Exception as e:
            create_transaction(
                request.user,
                amount / 100,
                "credit",
                "pending",
                "Wallet",
                payment_id,
            )
            messages.error(request, f"Error: {str(e)}")
            return render(request, "paymentfail.html")
    else:
        return HttpResponseBadRequest(
            "Only POST requests are allowed for this endpoint."
        )


def create_transaction(
    user, amount, transaction_type, payment_status, receiver, payment_id
):
    transaction = Transaction_detail(
        user=user,
        transaction_amount=amount,
        type=transaction_type,
        payment_status=payment_status,
        receiver_mobile=receiver,
        payment_id=payment_id,
    )
    transaction.save()


@transaction.atomic
def paymerchant(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            mobile = request.POST.get("mobile")
            amount = request.POST.get("amount")
            if float(amount) < 0:
                messages.error(request, "Enter valid Amount")
                return redirect("paymerchant")
            else:
                print(amount)
                wallet = Wallet.objects.filter(mobile=mobile).exists()
                if wallet:
                    with transaction.atomic():
                        wallet = Wallet.objects.select_for_update().get(user=user)
                        reciever_wallet = Wallet.objects.select_for_update().get(
                            mobile=mobile
                        )
                        if wallet.Wallet_amount < float(amount):
                            messages.error(request, "Insufficient Balance")
                            return redirect("/")
                        else:
                            wallet.Wallet_amount -= float(amount)
                            reciever_wallet.Wallet_amount += float(amount)
                            wallet.save()
                            reciever_wallet.save()
                    unique_id1 = get_random_string(length=12)
                    unique_id2 = get_random_string(length=13)
                    transaction.on_commit(
                        lambda: (
                            create_transaction(
                                request.user,
                                amount,
                                "debit",
                                "success",
                                mobile,
                                unique_id1,
                            ),
                            create_transaction(
                                reciever_wallet.user,
                                amount,
                                "credit",
                                "success",
                                wallet.mobile,
                                unique_id2,
                            ),
                        )
                    )
                    return render(request, "paymentsuccess.html")
                else:
                    messages.error(request, "User not Exists with this number")
                    return redirect("../paymerchant")
        return render(request, "paymerchant.html")
    return redirect("login")


def addwallet(request):
    user = request.user
    if user.is_authenticated:
        pass
    return render(request, "addwallet.html")


def transactionlist(request):
    user = request.user
    if user.is_authenticated:
        try:
            checkwallet = Wallet.objects.get(user=user)
            if checkwallet:
                transactionlist = Transaction_detail.objects.filter(user=user)
                return render(
                    request,
                    "transactionlist.html",
                    {"transactionlist": transactionlist},
                )
            else:
                return redirect("createwallet")
        except Wallet.DoesNotExist:
            return redirect("createwallet")
    else:
        return redirect("login")


def error_404_view(request, exception):
    status_code = 404
    message = "Page Not Found"
    return render(
        request, "errorpage.html", {"status_code": status_code, "message": message}
    )


def error_400_view(request, exception):
    status_code = 400
    message = "Bad Request"
    return render(
        request, "errorpage.html", {"status_code": status_code, "message": message}
    )


def error_500_view(request):
    status_code = 500
    message = "Server Error"
    return render(
        request, "errorpage.html", {"status_code": status_code, "message": message}
    )


def error_401_view(request):
    status_code = 401
    message = "Unauthorized User"
    return render(
        request, "errorpage.html", {"status_code": status_code, "message": message}
    )
