from django.contrib import admin
from .models import Post, Profile, admins
from .forms import AdminsCreationForm


admin.site.register(Post)
admin.site.register(Profile)


class AdminsAdmin(admin.ModelAdmin):
    form = AdminsCreationForm
    list_display = ["username", "password"]


admin.site.register(admins, AdminsAdmin)
