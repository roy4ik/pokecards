from django import forms
from django.views.generic.detail import DetailView
from .models import Trade, Vault, Counter_Offer
from .tcg_functions import shuffle_return7

class CardWidget(forms.CheckboxSelectMultiple):
    template_name='forms/test_template.html'

class TradeOffer(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['cards','public']
        widgets = {
            'cards': CardWidget()
        }

class CounterOfferForm(forms.ModelForm):
     class Meta:
        model = Counter_Offer
        fields = ['cards']
        widgets = {
            'cards': CardWidget()
        }
        