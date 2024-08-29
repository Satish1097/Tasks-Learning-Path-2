from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registration", views.registration, name="registration"),
    path("login", views.login, name="login"),
    path("createpost", views.createpost, name="createpost"),
    path("mypost", views.userpost, name="mypost"),
    path("logout", views.logout, name="logout"),
    path("editpost/<int:post_id>", views.editpost, name="editpost"),
    path("deletepost/<int:post_id>", views.deletepost, name="deletepost"),
]
