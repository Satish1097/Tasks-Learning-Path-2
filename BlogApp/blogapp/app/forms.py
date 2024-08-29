from django import forms
from django.contrib.auth.models import User
from .models import Post, Profile, admins
from django.contrib.auth.hashers import make_password


class registerationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    def clean_firstname(self):
        firstname = self.cleaned_data.get("first_name")
        if not firstname:
            raise forms.ValidationError()
        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data.get("last_name")
        if not lastname:
            raise forms.ValidationError()
        return lastname

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 5:
            raise forms.ValidationError()
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError()
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError()
        return make_password(password)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["Title", "file", "Description"]

        def clean_title(self):
            title = self.cleaned_data.get("Title")
            if not title:
                raise forms.ValidationError()
            return title

        def clean_file(self):
            file = self.cleaned_data.get("file")
            if not file:
                raise forms.ValidationError()
            return file

        def clean_description(self):
            description = self.clean_data.get("Description")
            if not description:
                raise forms.ValidationError()
            return description


class EditPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["Title", "file", "Description"]

    def clean_title(self):
        title = self.cleaned_data.get("Title")
        if not title:
            raise forms.ValidationError()
        return title

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if not file:
            raise forms.ValidationError()
        return file

    def clean_description(self):
        description = self.clean_data.get("Description")
        if not description:
            raise forms.ValidationError()
        return description


class AdminsCreationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = admins

        fields = ["username", "password"]

    def save(self, commit=True):

        admin = super().save(commit=False)

        admin.set_password(self.cleaned_data["password"])  # Hash the password

        if commit:

            admin.save()

        return admin
