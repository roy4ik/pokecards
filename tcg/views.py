from typing import Counter
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, ListView
import json
import requests
import random
from . import tcg
from tcg.forms import *
from .models import Pokemon, Color, Type, Species, Vault, Trade

#  functions


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
    user_vault = request.user.vault
    # 60 cards in a deck
    for pokemon_number in range(60):
        # get random card 
        pokeapi_url = f'https://pokeapi.co/api/v2/pokemon/{random.randint(1,893)}'
        # set max connections
        max_connections = 200
        try:
            print(pokeapi_url)
            pokemon = requests.get(pokeapi_url).json()
            tcg.is_in_db(pokemon['name'])
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
            user_deck.append(tcg.get_card_data(pokemon,species))
            # add to user's vault
            user_vault.pokemons.add(tcg.get_card_data(pokemon,species))
            print("adding legendary card")
        elif legendary == False:
            user_deck.append(tcg.get_card_data(pokemon,species))
            # add to user's vault
            user_vault.pokemons.add(tcg.get_card_data(pokemon,species))
            print('adding regular card')
        
        print(f"loading new deck : {'{:.2f}'.format(pokemon_number/60*100)}%")

    context.update({'user_deck': user_deck})
    print("user deck initialized")
    return "Success"


def vault(request):
    return render(request, 'vault.html')
    

def trade_select(request):
    context = {}
    shuffled_deck = tcg.shuffle_return7(request)
    context.update({
        'shuffled_deck': shuffled_deck
    })
    return render(request, 'forms/trade_select.html', context)

class CreateOffer(CreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateOffer,self).get_context_data(**kwargs)
        form = TradeOffer()
        form.fields['cards'].queryset = shuffle_return7(self.request)
        context['form'] = form
        return context
        
    def form_valid(self, form):
        print(form.cleaned_data)
        
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        self.object = form.save_m2m()
        # still getting error after save_m2m() 'NoneType' object has no attribute '__dict__'
        return HttpResponseRedirect(self.get_success_url())


    model = Trade
    form_class = TradeOffer
    template_name = 'forms/create_offer.html'
    success_url = 'vault'
    failed_message = "The user couldn't create Trade"

class TradeDetailView(DetailView):
    model = Trade
    template_name= 'trade_details.html'

class MyTrades(ListView):
    model = Trade
    template_name= 'my_trades.html'
    paginate_by = 100

class CreateCounterOffer(CreateView):
    def get_absolute_url(self):
        return reverse('tcg.views.TradeDetail', args=[str(self.pk)])

    def get_context_data(self, **kwargs):
        context = super(CreateCounterOffer,self).get_context_data(**kwargs)
        form = CounterOfferForm()
        form.fields['cards'].queryset = shuffle_return7(self.request)
        context['form'] = form
        return context
        
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.trade = self.get_absolute_url
        self.object.creator = self.request.user
        self.object.save()
        self.object = form.save_m2m()

        return HttpResponseRedirect(self.get_success_url())


    model = Counter_Offer
    form_class = CounterOfferForm
    template_name = 'forms/create_offer.html'
    success_url = ''
    failed_message = "The user couldn't create Trade"

