from .models import ProductCategory, Cart, Customer, Wishlist, CartItem
from django.db.models import F


def productcategory(request):
    user = request.user
    categories = ProductCategory.objects.all()
    product_in_cart = 0
    product_in_wishlist = 0
    cart_amount = 0
    if user.is_authenticated:
        customer = Customer.objects.get(customer=user)
        cart = Cart.objects.get(owner=customer)
        product_in_cart = cart.item.count()
        cart_items = CartItem.objects.annotate(
            product_amount=F("product__price") * F("quantity")
        ).filter(cart=cart)
        for i in cart_items:
            cart_amount += i.product_amount
        wishlist = Wishlist.objects.get(customer=customer)
        product_in_wishlist = wishlist.product.count()
    return {
        "categories": categories,
        "product_in_cart": product_in_cart,
        "product_in_wishlist": product_in_wishlist,
        "cart_amount": cart_amount,
    }
