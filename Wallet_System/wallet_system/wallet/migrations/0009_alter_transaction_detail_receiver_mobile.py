# Generated by Django 5.0.7 on 2024-09-23 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0008_transaction_detail_receiver_mobile_wallet_mobile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_detail',
            name='receiver_mobile',
            field=models.CharField(max_length=13),
        ),
    ]
