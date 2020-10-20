from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from accounts.models import Profile
import json
import requests
# Create your views here.
def all_cards(request):
    context = {}
    context['all_pokemon'] = requests.get("pokemon")
    return render (request, 'all_cards.html', context)