from .models import ProductCategory, Customer, Wishlist, CartItem, Order, OrderItem
from django.db.models import F


def productcategory(request):
    user = request.user
    categories = ProductCategory.objects.all()
    product_in_cart = 0
    product_in_wishlist = 0
    cart_amount = 0
    order = 0
    if user.is_authenticated:
        order = Order.objects.filter(user=user, shipment_status=False).count()
        customer = Customer.objects.get(customer=user)
        # cart = Cart.objects.get(owner=customer)
        cart_items = CartItem.objects.annotate(
            product_amount=F("product__price") * F("quantity")
        ).filter(user=user)
        product_in_cart = cart_items.count()
        for i in cart_items:
            cart_amount += i.product_amount
        wishlist = Wishlist.objects.get(customer=customer)
        product_in_wishlist = wishlist.product.count()
    return {
        "categories": categories,
        "product_in_cart": product_in_cart,
        "product_in_wishlist": product_in_wishlist,
        "cart_amount": cart_amount,
        "order": order,
    }
