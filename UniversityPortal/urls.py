# project/urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from accounts.api import api  # Import the shared API instance

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),  # This now includes both JWT endpoints and login_student

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
