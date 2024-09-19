from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class registerationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    def clean_firstname(self):
        firstname = self.cleaned_data.get("first_name")
        if not firstname:
            raise forms.ValidationError("firstname required")
        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data.get("last_name")
        if not lastname:
            raise forms.ValidationError("lastname required")
        return lastname

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 5:
            raise forms.ValidationError("username required")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("email required")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("password required")
        return make_password(password)
