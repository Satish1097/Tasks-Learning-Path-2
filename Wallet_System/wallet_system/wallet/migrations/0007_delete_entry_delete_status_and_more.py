# Generated by Django 5.0.7 on 2024-09-22 11:55

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0006_status_transaction_detail_payment_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Entry',
        ),
        migrations.DeleteModel(
            name='Status',
        ),
        migrations.AlterField(
            model_name='transaction_detail',
            name='TransactionId',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction_detail',
            name='payment_status',
            field=models.CharField(choices=[('success', 'Success'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='transaction_detail',
            name='type',
            field=models.CharField(choices=[('debit', 'Debit'), ('credit', 'Credit')], default='debit', max_length=6),
        ),
    ]