from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True)
    profile_picture = models.ImageField(
        upload_to="images/", default="static/images/default-user.png"
    )

    def __str__(self):
        return self.customer.username


class ProductCategory(models.Model):
    categoryname = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media/", default="null")

    def __str__(self):
        return self.categoryname


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory, on_delete=models.DO_NOTHING, related_name="category"
    )
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to="meadia/")
    stock = models.PositiveIntegerField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product_in_sale(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    discounted_price = models.FloatField()


class Cart(models.Model):
    owner = models.OneToOneField(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.customer.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="item")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Wishlist(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return self.customer.customer.username


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.customer.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class TransactionDetail(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.FloatField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.customer.username


class Blogpost(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="media/")
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Reviewed_product(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, default=" ")


class Message(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name


class Billing_Address(models.Model):
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Address = models.TextField()
    City = models.CharField(max_length=100)
    PinCode = models.CharField(max_length=20)
    Email = models.EmailField()
    phone = models.CharField(max_length=13)


@receiver(post_save, sender=User)
def createcustomer(sender, instance, created, **kwargs):
    if created:
        customer = Customer.objects.create(customer=instance, address=" ")
        Cart.objects.create(user=instance)
        Wishlist.objects.create(customer=customer)
        Reviewed_product.objects.create(user=instance)
