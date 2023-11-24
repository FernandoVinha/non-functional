# config/urls.py

from django.contrib import admin
from django.urls import include, path


# Adicione 'rest_framework' como um namespace
app_name = 'rest_framework'



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('account.urls')),
]
