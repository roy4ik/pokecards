from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, CharField, IntegerField, URLField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Color(models.Model):
    name = CharField(max_length=100)
    url  = URLField()

class Type(models.Model):
    name = CharField(max_length=100)
    url  = URLField()

class Species(models.Model):
    name = CharField(max_length=255)
    base_experience= IntegerField()
    url  = URLField()
    color = ForeignKey(Color, on_delete=models.CASCADE())
    type = ForeignKey(Type, on_delete=models.CASCADE())

class Pokemon(models.Model):
    name = CharField(max_length=255)
    rarity = IntegerField(min(0))
    weight = IntegerField
    img_url = URLField()
    species = ForeignKey(Species, on_delete=models.CASCADE())


class Offer(models.Model):
    pokemon1 = ForeignKey(Pokemon, on_delete=models.PROTECT(),null=True)
    pokemon2 = ForeignKey(Pokemon, on_delete=models.PROTECT(),null=True)
    pokemon3 = ForeignKey(Pokemon, on_delete=models.PROTECT(),null=True)
    pokemon4 = ForeignKey(Pokemon, on_delete=models.PROTECT(),null=True)
    
class Trades(models.Model):
    user1 = ForeignKey(User, on_delete=models.PROTECT(),null=True)
    user2 = ForeignKey(User, on_delete=models.PROTECT(),null=True)
    offer1 = ForeignKey(Offer,on_delete=models.PROTECT(),null=True)
    offer2 = ForeignKey(Offer,on_delete=models.PROTECT(),null=True)
    completed = BooleanField()
    retracted = BooleanField()


class Vault(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL())
    pokemons = models.ManyToManyField(Pokemon)
    pokemons = models.ManyToManyField(Pokemon)
    total_xp = IntegerField()

    