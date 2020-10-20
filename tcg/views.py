from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from requests import status_codes
from accounts.models import Profile
import json
import requests
import random

#  functions

def add_card(pokeapi_url, card):
    '''
    gets the card info from the api
    '''
    print(f'Updating {pokeapi_url} at {card}')
    card.update({
    'name' : requests.get(pokeapi_url).json()['forms'][0]['name'],
    'weight' : requests.get(pokeapi_url).json()['weight'],
    'img' : requests.get(pokeapi_url).json()['sprites']['front_default'],
    'type' : requests.get(pokeapi_url).json()['types'][0]['type']['name'],
    'species' : requests.get(pokeapi_url).json()['species']['name'],
    'color' : requests.get(requests.get(pokeapi_url).json()['species']['url']).json()['color']['name'],
    'is_legendary' : requests.get(requests.get(pokeapi_url).json()['species']['url']).json()['is_legendary'] 
    })


# Create your views here.
def all_cards(request):
    context = {}
    try:
        all_pokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1050").json()['results']
        for pokemon in range(1,len(all_pokemon)-1):
            img_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{pokemon}.png'
            all_pokemon[pokemon-1].update({'img' : img_url})
        context.update({'all_pokemon': all_pokemon})
    except ConnectionError:
        error_msg = "Oops couldn't connect to the API"
        context.update({'all_pokemon': error_msg})
    finally: 
        return render (request, 'all_cards.html', context)

def vault_new(request):
    context = {}
    try:
        user_deck = []
        # 60 cards in a deck
        for pokemon in range(1,60):
            # get random card 
            pokeapi_url = f'https://pokeapi.co/api/v2/pokemon/{random.randint(1,1050)}'
            print(requests.get(pokeapi_url))
            legendary_counter = 0
            # check if legendary card - max 5 per user
            if requests.get(requests.get(pokeapi_url).json()['species']['url']).json()['is_legendary'] == True and legendary_counter < 5:
                legendary_counter += 1
                print("adding legendary card")
                add_card(pokeapi_url, user_deck[pokemon-1])
            elif requests.get(requests.get(pokeapi_url).json()['species']['url']).json()['is_legendary'] == False:
                print('adding regular card')
                add_card(pokeapi_url, user_deck[pokemon-1])
                
        print("user deck initialized")
        context.update({'user_deck': user_deck})
    except ConnectionError:
        error_msg = "Oops couldn't connect to the API"
        context.update({'user_deck': error_msg})
    finally: 
        return render (request, 'vault.html', context)