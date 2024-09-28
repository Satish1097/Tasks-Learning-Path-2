from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("wallet.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "wallet.views.error_404_view"
handler400 = "wallet.views.error_400_view"
handler500 = "wallet.views.error_500_view"
handler401 = "wallet.views.error_401_view"
