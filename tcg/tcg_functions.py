import random
import requests
from . import models

def vault_new(vault):
    # 60 cards in a deck
    for pokemon_number in range(60):
        # get random card 
        pokeapi_url = f'https://pokeapi.co/api/v2/pokemon/{random.randint(1,893)}'
        # set max connections
        max_connections = 200
        try:
            print(pokeapi_url)
            pokemon = requests.get(pokeapi_url).json()
            is_in_db(pokemon['name'])
            species = requests.get(pokemon['species']['url']).json()
        except requests.HTTPError:
            if pokemon_number > 0 and max_connections > 0:
                pokemon_number -=1
                max_connections -=1
            print("Connection Error - trying again")
            continue
        except TypeError:
            # used on Json error
            if pokemon_number > 0 and max_connections > 0:
                pokemon_number -=1
                max_connections -=1
            print("Connection Error - trying again")
            continue
        legendary = species['is_legendary']
        legendary_counter = 0

        # check if legendary card - max 5 per user
        if legendary == True and legendary_counter < 5:
            legendary_counter += 1
            # add to user's vault
            vault.pokemons.add(get_card_data(pokemon,species))
            print("adding legendary card")
        elif legendary == False:
            # add to user's vault
            vault.pokemons.add(get_card_data(pokemon,species))
            print('adding regular card')
        
        print(f"loading new deck : {'{:.2f}'.format(pokemon_number/60*100)}%")
    print("user deck initialized")
    return "Success"


def shuffle_return7(request):
    deck = list(request.user.vault.pokemons.all())
    random.shuffle(deck)
    qs = request.user.vault.pokemons.filter(id__in=[card.id for card in deck[0:7]])
    return qs
    

def get_card_data(pokemon,species):
    '''
    gets card details from the db or the api and returns it in dict
    # params: pokeapi_url: url to pokeapi endpoint
    # returns card(dict)
    '''
    if is_in_db(pokemon['name']) == False:
        api_card = get_card_api(pokemon,species)
        card = add_card(api_card)
    else:
        card = models.Pokemon.objects.get(name=pokemon['name'])
    return card


def get_card_api(pokemon,species):
    '''
    gets card details from pokeapi and returns it in dict
    # params: pokeapi_url: url to pokeapi endpoint
    # returns card(dict)
    '''
    if is_in_db(pokemon['name']) == False:
        card = {}
        # print(f'getting {pokemon}')
        card.update({
        'name' : pokemon['name'],
        'weight' : pokemon['weight'],
        'img' : pokemon['sprites']['front_default'],
        'type' : pokemon['types'][0]['type']['name'],
        'species' : pokemon['species']['name'],
        'base_experience':pokemon['base_experience'],
        'color' : species['color']['name'],
        'is_legendary' : species['is_legendary'] 
        })
        return card

def add_card(card):
    """
    adds card to db
    #params: card (from api)
    #returns: pokemon obj.
    """
    # adding color
    color, created = models.Color.objects.get_or_create(name=card['color'])
    print("type got created in db")
    #  adding Type
    type, created = models.Type.objects.get_or_create(name=card['type'])
    print("type got created in db")
    #  adding Species
    species, created = models.Species.objects.get_or_create(name=card['name'], color=color, type=type)
    print("species got created in db")
    #   adding Pokemon
    pokemon, created = models.Pokemon.objects.get_or_create(name=card['name'], base_experience=card['base_experience'], weight=card['weight'], img_url=card['img'], species= species, is_legendary = card['is_legendary'])
    print("pokemon got created in db")
    return pokemon


def is_in_db(pokemon_name):
    """
    checks whether card is in database already
    #params: pokemon_name(str) the name of the pokemon
    #returns: returns bool
    """
    try:
        in_db = models.Pokemon.objects.get(name=pokemon_name)
        return True
    except:
        return False
    
