from django.db import models
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver


class Ingredient(models.Model):
    name = models.TextField(max_length=100)


class Allergen(models.Model):
    name = models.TextField(max_length=100)


class UserPage(models.Model):
    user = models.OneToOneField('auth.user')
    userhandle = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='profile_photos', name='photo', blank=True, null=True)
    description = models.CharField(max_length=350, null=True, blank=True)

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        return "http://vignette3.wikia.nocookie.net/shokugekinosoma/images/6/60/No_Image_Available.png/revision/latest?cb=20150708082716"


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    instruction = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)
    allergens = models.ManyToManyField(Allergen)


@receiver(post_save, sender='auth.user')
def create_userpage(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        UserPage.objects.create(user=instance)


@receiver(post_save, sender='auth.user')
def create_usertoken(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        Token.objects.create(user=instance)