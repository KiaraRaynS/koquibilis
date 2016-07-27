from django.db import models
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey('auth.user')


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    instruction = models.TextField()
    ingredients = models.TextField()


class SavedRecipe(models.Model):
    title = models.CharField(max_length=100)
    recipe_key = models.CharField(max_length=200)
    ingredients = models.TextField()
    note = models.TextField(null=True, blank=True)
    small_image = models.TextField(max_length=200)
    big_image = models.TextField(max_length=200)
    user = models.ForeignKey('auth.user')


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
