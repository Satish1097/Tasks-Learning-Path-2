from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=13, blank=False, null=False, unique=True)
    Wallet_amount = models.FloatField(default="0")
    profile_picture = models.ImageField(
        upload_to="media/", default="static/image/default-user.png"
    )

    def __str__(self):
        return self.user.username


class Transaction_detail(models.Model):
    TYPE_CHOICES = (
        ("debit", "Debit"),
        ("credit", "Credit"),
    )

    STATUS_CHOICES = (
        ("success", "Success"),
        ("failed", "Failed"),
        ("pending", "Pending"),
    )

    TransactionId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_amount = models.FloatField()
    type = models.CharField(max_length=6, choices=TYPE_CHOICES, default="debit")
    payment_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending"
    )
    receiver_mobile = models.CharField(max_length=13, blank=False, null=False)
    date_of_transaction = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return self.user.username


# @receiver(post_save, sender=User)
# def createwallet(sender, instance, created, **kwargs):
#     if created:
#         Wallet.objects.create(user=instance)
