from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(TransactionDetail)
admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Blogpost)
admin.site.register(Product_in_sale)
admin.site.register(Wishlist)
admin.site.register(Reviewed_product)
admin.site.register(Billing_Address)
