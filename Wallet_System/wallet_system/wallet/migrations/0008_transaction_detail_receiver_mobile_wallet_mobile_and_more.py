# Generated by Django 5.0.7 on 2024-09-23 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0007_delete_entry_delete_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction_detail',
            name='receiver_mobile',
            field=models.CharField(default='', max_length=13, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wallet',
            name='mobile',
            field=models.CharField(default=' ', max_length=13, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wallet',
            name='profile_picture',
            field=models.ImageField(default='static/image/default-user.png', upload_to='media/'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
