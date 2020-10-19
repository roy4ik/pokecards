from django.urls import path, include
import django.contrib.auth.urls
from .views import *

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
]
