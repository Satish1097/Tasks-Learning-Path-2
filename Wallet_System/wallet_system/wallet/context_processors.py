from .models import Wallet
from django.shortcuts import redirect


def getprofile(request):
    user = request.user
    context_data = {}  # Initialize an empty context dictionary
    if user.is_authenticated:
        try:
            wallet = Wallet.objects.get(user=user)
            context_data = {
                "wallet": wallet,
            }
        except Wallet.DoesNotExist:
            context_data["redirect_to_createwallet"] = (
                True  # Flag to signal redirection
            )
    else:
        context_data["redirect_to_login"] = True  # Flag to signal login redirection

    return context_data  # Return the context dictionary
