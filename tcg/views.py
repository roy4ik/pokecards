from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from requests import status_codes
from accounts.models import Profile
import json
import requests
import random

#  functions

def get_card(pokemon,species):
    '''
    gets card details from pokeapi and returns it in dict
    # params: pokeapi_url: url to pokeapi endpoint
    # returns card(dict)
    '''
    card = {}
    # print(f'getting {pokemon}')
    card.update({
    'name' : pokemon['name'],
    'weight' : pokemon['weight'],
    'img' : pokemon['sprites']['front_default'],
    'type' : pokemon['types'][0]['type']['name'],
    'species' : pokemon['species']['name'],
    'color' : species['color']['name'],
    'is_legendary' : species['is_legendary'] 
    })
    return card


# Create your views here.
def all_cards(request):
    context = {}
    try:
        all_pokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1050").json()['results']
        for pokemon in range(1,len(all_pokemon)-1):
            img_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{pokemon}.png'
            all_pokemon[pokemon-1].update({'img' : img_url})
        context.update({'all_pokemon': all_pokemon})
    except requests.HTTPError:
        error_msg = "all_cards Oops couldn't connect to the API"
        context.update({'all_pokemon': error_msg})
    finally: 
        return render (request, 'all_cards.html', context)

def vault_new(request):
    context = {}
    user_deck = []

    # 60 cards in a deck
    for pokemon_number in range(60):
        # get random card 
        pokeapi_url = f'https://pokeapi.co/api/v2/pokemon/{random.randint(1,893)}'
        try:
            print(pokeapi_url)
            pokemon = requests.get(pokeapi_url).json()
            species = requests.get(pokemon['species']['url']).json()
        except requests.HTTPError:
            if pokemon_number > 0:
                pokemon_number -=1
            print("Connection Error - trying again")
            continue
            
        legendary = species['is_legendary']
        legendary_counter = 0

        # check if legendary card - max 5 per user
        if legendary == True and legendary_counter < 5:
            legendary_counter += 1
            user_deck.append(get_card(pokemon,species))
            print("adding legendary card")
        elif legendary == False:
            user_deck.append(get_card(pokemon,species))
            print('adding regular card')
        
        print(f"loading new deck : {'{:.2f}'.format(pokemon_number/60*100)}%")

    context.update({'user_deck': user_deck})
    print("user deck initialized")
    return render (request, 'vault_new.html', context)