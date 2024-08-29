from django.shortcuts import render, redirect, get_object_or_404
from .forms import registerationForm, PostForm, EditPost
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Post, Profile, admins


def index(request):
    posts = Post.objects.filter(block_status=False).order_by("-created_on")
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page")
    posts_paginator = paginator.get_page(page_number)
    return render(
        request, "home.html", {"posts": posts, "posts_paginator": posts_paginator}
    )


def registration(request):
    if request.method == "POST":
        form = registerationForm(request.POST)
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if len(username) < 5:
            messages.error(request, "username must have 5 charater or more")
        elif len(password) < 8:
            messages.error(request, "password must have 8 digit or more")
        elif password == username:
            messages.error(request, "password should not same as  username")
        elif password == firstname:
            messages.error(request, "password should not same as  firstname")
        elif password == lastname:
            messages.error(request, "password should not same as  lastname")
        elif form.is_valid():
            form.save()
            messages.success(request, "Successfully Registered")
            return redirect("login")
    else:
        form = registerationForm()
    return render(request, "registration.html", {"form": form})


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            messages.success(request, "Login Successfully")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credential")
            return redirect("../login")
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/login")


#                                      Post section
def createpost(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = user
                post.save()
                messages.success(request, "Post Created Successfully")
                return redirect("/")
        else:
            form = PostForm()
        return render(request, "postform.html", {"form": form})
    else:
        return redirect("login")


def editpost(request, post_id):
    user = request.user
    if user.is_authenticated:
        post = get_object_or_404(Post, id=post_id, user=request.user)
        if request.method == "POST":
            form = EditPost(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, "Updated Successfully")
                return redirect("/")
        else:
            form = EditPost(instance=post)
        return render(request, "editpost.html", {"form": form})
    else:
        return redirect("login")


def deletepost(request, post_id):
    user = request.user
    if user.is_authenticated:
        post = get_object_or_404(Post, id=post_id, user=request.user)
        post.delete()
        messages.success(request, "deleted successfully")
        return redirect("/")
    else:
        return redirect("login")


def userpost(request):
    user = request.user
    if user.is_authenticated:
        posts = Post.objects.filter(user=user)
        return render(request, "mypost.html", {"posts": posts})
    else:
        return redirect("login")


def error_404_view(request, exception):
    status_code = 404
    message = "Page Not Found"
    return render(
        request, "errorpage.html", {"status_code": status_code, "message": message}
    )


def error_400_view(request, exception):
    status_code = 400
    message = "Bad Request"
    return render(
        request, "errorpage.html", {"status_code": status_code, "message": message}
    )


def error_500_view(request):
    status_code = 500
    message = "Server Error"
    return render(
        request, "errorpage.html", {"status_code": status_code, "message": message}
    )
