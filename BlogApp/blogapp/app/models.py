from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.contrib.auth.hashers import make_password, check_password


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="media/")
    Title = models.CharField(max_length=100)
    Description = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    block_status = models.BooleanField(default=False)

    def __str__(self):
        return self.Title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="media/", default="app/static/images/default-user.png"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class admins(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.password
