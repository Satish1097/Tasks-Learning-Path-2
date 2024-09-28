from django.core.management.base import BaseCommand
from wallet.models import Transaction_detail, Wallet
from django.db.models import Q
import razorpay


class Command(BaseCommand):
    help = "Update status of payment"

    def handle(self, *args, **options):
        pending_payments = Transaction_detail.objects.filter(payment_status="pending")

        # Check if there are any pending payments
        if not pending_payments.exists():
            self.stdout.write(
                self.style.WARNING("No pending or failed payments found.")
            )
            return

        for pending in pending_payments:
            client = razorpay.Client(
                auth=("rzp_test_dAeKznpfJoVqVt", "OA8xXFOj9pRlxQq0SmHe5KEc")
            )
            payment_details = client.payment.fetch(pending.payment_id)
            print(payment_details)
            if payment_details.get("status") == "captured":
                pending.payment_status = "success"
                pending.save()
                wallet = Wallet.objects.get(user=pending.user)
                wallet.Wallet_amount += pending.transaction_amount
                wallet.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Status updated for ID {pending.TransactionId}")
                )
        self.stdout.write(self.style.SUCCESS("Status updation completed."))
