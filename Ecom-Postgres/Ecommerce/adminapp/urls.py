from django.urls import path
from adminapp import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("userlists", views.userlists, name="userlists"),
    path("orderlists", views.orderlists, name="orderlists"),
    path("itemlists", views.itemlists, name="itemlists"),
]
