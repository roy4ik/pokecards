import random
from . import views
#functions for tcg views
def get_user_vault(request):
    user_vault = views.Vault.objects.get(user=request.user)

    return user_vault

def shuffle_return7(request):
    deck = list(get_user_vault(request).pokemons.all())
    random.shuffle(deck)
    return deck[0:7]

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
        card = views.Pokemon.objects.get(name=pokemon['name'])
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
    color, created = views.Color.objects.get_or_create(name=card['color'])
    print("type got created in db")
    #  adding Type
    type, created = views.Type.objects.get_or_create(name=card['type'])
    print("type got created in db")
    #  adding Species
    species, created = views.Species.objects.get_or_create(name=card['name'], color=color, type=type)
    print("species got created in db")
    #   adding Pokemon
    pokemon, created = views.Pokemon.objects.get_or_create(name=card['name'], base_experience=card['base_experience'], weight=card['weight'], img_url=card['img'], species= species, is_legendary = card['is_legendary'])
    print("pokemon got created in db")
    return pokemon


def is_in_db(pokemon_name):
    """
    checks whether card is in database already
    #params: pokemon_name(str) the name of the pokemon
    #returns: returns bool
    """
    try:
        in_db = views.Pokemon.objects.get(name=pokemon_name)
        return True
    except:
        return False
    
