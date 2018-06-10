from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('air/', include('air.urls')),
    path('admin/', admin.site.urls),
]