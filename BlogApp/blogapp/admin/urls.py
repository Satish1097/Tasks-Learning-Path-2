from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_admin, name="login_admin"),
    path("logout_admin", views.logout_admin, name="logout_admin"),
    path("adminpanel", views.adminpannel, name="adminpanel"),
    path("blockpost/<int:post_id>", views.blockpost, name="blockpost"),
    path("postedit/<int:post_id>", views.editpost, name="postedit"),
    path("postdelete/<int:post_id>", views.deletepost, name="postdelete"),
    path("userlist", views.userlist, name="userlist"),
    path("blockuser/<int:user_id>", views.blockuser, name="blockuser"),
]
