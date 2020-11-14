from django.contrib import admin
from django.urls import path
from package_system import views

urlpatterns = [
    path('admin/', admin.site.urls),
]
