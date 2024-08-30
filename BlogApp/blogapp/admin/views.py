from django.shortcuts import render, redirect
from app.models import Post, admins
from django.core.paginator import Paginator
from django.contrib import messages
from app.forms import EditPost
from django.contrib.auth.models import User
from django.db.models.functions import Lower


def login_admin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        try:
            admin_user = admins.objects.get(username=username)
            if admin_user.check_password(password):
                request.session["user"] = admin_user.id
                return redirect("adminpanel")
            else:
                messages.error(request, "Invalid Credential")
                return render(request, "login_admin.html")
        except admins.DoesNotExist:
            message = "Invalid credentials"
            return render(request, "login_admin.html", {"message": message})
    return render(request, "login_admin.html")


def logout_admin(request):
    del request.session["user"]
    return redirect("login_admin")


def adminpannel(request):
    user = request.session.get("user")
    print(user)
    if user is not None:
        posts = Post.objects.filter(block_status=False).order_by("-created_on")
        paginator = Paginator(posts, 6)
        page_number = request.GET.get("page")
        posts_paginator = paginator.get_page(page_number)
        return render(request, "Dashboard.html", {"posts_paginator": posts_paginator})
    else:
        return redirect("login_admin")


def blockpost(request, post_id):
    user = request.session.get("user")
    try:
        post = Post.objects.get(id=post_id)
        if post and user:
            post.block_status = True
            post.save()
            return redirect("adminpanel")
    except Post.DoesNotExist:
        messages.error(request, "Post not found with this id")
        return redirect("adminpanel")


def editpost(request, post_id):
    user = request.session.get("user")
    if user is not None:
        try:
            post = Post.objects.get(id=post_id)
            if request.method == "POST":
                form = EditPost(request.POST, request.FILES, instance=post)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Updated Successfully")
                    return redirect("adminpanel")
            else:
                form = EditPost(instance=post)
            return render(request, "posteditadmin.html", {"form": form})
        except Post.DoesNotExist:
            messages.error(request, "Post not found")
            return redirect("adminpanel")
    else:
        return redirect("login_admin")


def deletepost(request, post_id):
    user = request.session.get("user")
    if user is not None:
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            messages.success(request, "deleted successfully")
            return redirect("adminpanel")
        except Post.DoesNotExist:
            messages.error(request, "Post does not exist")
            return redirect("adminpanel")
    else:
        return redirect("login_admin")


def userlist(request):
    user = request.session.get("user")
    if user is not None:
        users = (
            User.objects.exclude(is_superuser=True)
            .filter(is_active=True)
            .order_by(Lower("username"))
        )
        paginator = Paginator(users, 10)
        page_number = request.GET.get("page")
        users_paginator = paginator.get_page(page_number)
        return render(
            request,
            "userlist.html",
            {
                "users_paginator": users_paginator,
            },
        )
    else:
        return redirect("login_admin")


def blockuserlist(request):
    user = request.session.get("user")
    if user is not None:
        blocked_users = User.objects.filter(is_active=False).order_by(Lower("username"))
        paginator = Paginator(blocked_users, 10)
        page_number = request.GET.get("page")
        blocked_users_paginator = paginator.get_page(page_number)
        return render(
            request,
            "blockeduser.html",
            {
                "blocked_users_paginator": blocked_users_paginator,
            },
        )
    else:
        return redirect("login_admin")


def blockuser(request, user_id):
    user = request.session.get("user")
    if user is not None:
        try:
            user = User.objects.get(id=user_id)
            user.is_active = False
            user.save()
            messages.success(request, "Blocked")
            return redirect("blockuserlist")
        except User.DoesNotExist:
            messages.error(request, "user does not exist")
            return redirect("adminpanel")
    else:
        return redirect("login_admin")


def unblockuser(request, user_id):
    user = request.session.get("user")
    if user is not None:
        try:
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            messages.success(request, "unblocked")
            return redirect("userlist")
        except User.DoesNotExist:
            messages.error(request, "user does not exist")
            return redirect("adminpanel")
    else:
        return redirect("login_admin")
