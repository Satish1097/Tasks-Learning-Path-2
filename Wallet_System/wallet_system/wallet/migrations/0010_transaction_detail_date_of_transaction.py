# Generated by Django 5.0.7 on 2024-09-23 12:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0009_alter_transaction_detail_receiver_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction_detail',
            name='date_of_transaction',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]