from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Wallet


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


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ["mobile", "profile_picture"]
        widgets = {
            "mobile": forms.TextInput(
                attrs={"placeholder": "Enter your mobile number"}
            ),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        if not mobile:
            raise forms.ValidationError("mobile number is required")
        # elif len(mobile) < 10:
        #     raise forms.ValidationError("Enter valid Number")
        return mobile

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get("profile_picture")
        if not profile_picture:
            raise forms.ValidationError("profile_picture required")
        return profile_picture


# class add_amountForm(forms.ModelForm):
#     class Meta:
#         model = Wallet
#         fields = ["Wallet_amount"]

#     def clean_amount(self):
#         amount = self.cleaned_data.get("Wallet_amount")
#         if not amount:
#             raise forms.ValidationError("Enter Amount")
#         return amount
