from django.core.management.base import BaseCommand
from wallet.models import *


class Command(BaseCommand):
    help = "update status of payment"

    def handle(self, *args, **options):
        pending_payment = Transaction_detail.objects.filter(status="pending")

        for pending in pending_payment:
            pending.payment_status = "success"
            pending.save()

            self.stdout.write(self.style.SUCCESS("Status Updated for ID "))
        self.stdout.write(self.style.SUCCESS("Status Updation Completed"))
