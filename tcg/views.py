from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from requests import status_codes
from accounts.models import Profile
import json
import requests
# Create your views here.
def all_cards(request):
    context = {}
    try:
        all_pokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1050").json()['results']
        for pokemon in range(1,len(all_pokemon)-1):
            img_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{pokemon}.png'
            # print(img_url)
            all_pokemon[pokemon-1].update({'img' : img_url})
            # pokeapi_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
            # print(requests.get(pokeapi_url))
            # print(f'Updating {pokeapi_url} at {all_pokemon[pokemon-1]}')
            # all_pokemon[pokemon-1].update({'weight' : requests.get(pokeapi_url).json()['weight'],
            # 'img' : requests.get(pokeapi_url).json()['sprites']['front_default'],
            # 'type' : requests.get(pokeapi_url).json()['types'][0]['type']['name'],
            # 'species' : requests.get(pokeapi_url).json()['species']['name'],
            # 'color' : requests.get(requests.get(pokeapi_url).json()['species']['url']).json()['color']['name']})
            # print(f"Pokemon List {'{:.2f}'.format((pokemon/len(all_pokemon)*100))}% updated")
        context.update({'all_pokemon': all_pokemon})
    except ConnectionError:
        error_msg = "Oops couldn't connect to the API"
        context.update({'all_pokemon': error_msg})
    finally: 
        return render (request, 'all_cards.html', context)