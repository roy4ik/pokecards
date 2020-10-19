from django.urls import path, include
import django.contrib.auth.urls
from .views import *


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', LoginView.as_view(template_name='base/base.html'), name ='login'),
    path('/signUp', SignUp.as_view(template_name = 'registration/signUp.html'), name='SignUp'),
    path('/logout', LogoutView.as_view(template_name='base/base.html'), name ='logout'),
    path('/profile/update', ProfileUpdate.as_view(), name='profileupdate')
]
