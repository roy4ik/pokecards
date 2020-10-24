from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='usr/profile/img/', default='usr/profile/default/pokeball-15.png')


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)



