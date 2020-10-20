from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from requests import status_codes
from accounts.models import Profile
import json
import requests
# Create your views here.
def all_cards(request):
    try:
        all_pokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100&offset=200").json[2]
        context = {}
        context.update({'all_pokemon': all_pokemon})
        print(context['all_pokemon'])
    except ConnectionError:
        error_msg = "Oops couldn't connect to the API"
    finally: 
        return render (request, 'all_cards.html', context)