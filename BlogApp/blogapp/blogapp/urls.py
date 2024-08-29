from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls")),
    path("admins/", include("admin.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "app.views.error_404_view"
handler400 = "app.views.error_400_view"
handler500 = "app.views.error_500_view"
