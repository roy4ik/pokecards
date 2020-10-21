from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, CharField, DateField, IntegerField, URLField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Color(models.Model):
    name = CharField(max_length=100)
    url  = URLField(null=True)

class Type(models.Model):
    name = CharField(max_length=100)
    url  = URLField(null=True)

class Species(models.Model):
    name = CharField(max_length=255)
    url  = URLField(null = True)
    color = ForeignKey(Color, on_delete=models.CASCADE)
    type = ForeignKey(Type, on_delete=models.CASCADE)

class Pokemon(models.Model):
    name = CharField(max_length=255)
    base_experience= IntegerField(null =True)
    weight = IntegerField(null =True)
    img_url = URLField(null =True)
    species = ForeignKey(Species, on_delete=models.CASCADE)
    is_legendary = BooleanField(null =True)


class Offer(models.Model):
    pokemons = ManyToManyField(Pokemon)

class Counter_Offer(models.Model):
    pokemons = ManyToManyField(Pokemon)
    
class Trades(models.Model):
    users = ManyToManyField(User)
    offer = models.OneToOneField(Counter_Offer,on_delete=models.PROTECT,null=True)
    counter_offer = models.OneToOneField(Offer,on_delete=models.PROTECT,null=True)
    date_created = DateField(auto_now_add=True)
    date_completed = DateField(auto_now=True)
    completed = BooleanField(default=False)
    retracted = BooleanField(default=False)
    public = BooleanField(default=False)


class Vault(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    pokemons = models.ManyToManyField(Pokemon)
    total_xp = IntegerField(null=True)


@receiver(post_save, sender=User)
def create_vault(sender, created, instance, **kwargs):
    if created:
        profile = Vault.objects.create(user=instance)


@receiver(post_save, sender=Trades)
def create_vault(sender, created, instance, **kwargs):
    if created:
        profile = Offer.objects.create(trades=instance)

@receiver(post_save, sender=Trades)
def create_vault(sender, created, instance, **kwargs):
    if created:
        profile = Counter_Offer.objects.create(trades=instance)