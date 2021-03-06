from django.db import models
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserPage(models.Model):
    user = models.OneToOneField('auth.user')
    photo = models.ImageField(upload_to='profile_photos', name='photo', blank=True, null=True)
    description = models.CharField(max_length=350, null=True, blank=True)
    bookmarks_private = models.BooleanField(default=False)
    uploads_private = models.BooleanField(default=False)

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return "http://vignette3.wikia.nocookie.net/shokugekinosoma/images/6/60/No_Image_Available.png/revision/latest?cb=20150708082716"


class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    measurementunit = models.CharField(max_length=15, null=True, blank=True)
    user = models.ForeignKey('auth.user')
    last_edit = models.DateTimeField(auto_now_add=True)


class ShoppingList(models.Model):
    user = models.ForeignKey('auth.user')
    ingredients = models.TextField(null=True, blank=True)


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    instruction = models.TextField()
    ingredients = models.TextField()
    detailed_ingredients = models.TextField()


class SavedRecipe(models.Model):
    title = models.CharField(max_length=100)
    recipe_key = models.CharField(max_length=200)
    ingredients = models.TextField()
    note = models.TextField(null=True, blank=True)
    small_image = models.TextField(max_length=200)
    big_image = models.TextField(max_length=200)
    user = models.ForeignKey('auth.user')
    bookmark_date = models.DateTimeField(auto_now_add=True)
    detailed_ingredients = models.TextField()


class UserUploadedRecipe(models.Model):
    user = models.ForeignKey('auth.user')
    title = models.CharField(max_length=100)
    basic_ingredients = models.TextField()
    detailed_ingredients = models.TextField(null=True, blank=True)
    uploader_notes = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    recipe_link = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos', name='recipephoto', blank=True, null=True)


class UploadedRecipeBookmark(models.Model):
    user = models.ForeignKey('auth.user')
    title = models.CharField(max_length=100)
    bookmark_notes = models.CharField(max_length=200, null=True, blank=True)
    recipe = models.ForeignKey(UserUploadedRecipe)
    bookmark_date = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender='auth.user')
def create_userpage(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        UserPage.objects.create(user=instance)


@receiver(post_save, sender='auth.user')
def create_shoppinglist(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        ShoppingList.objects.create(user=instance)


@receiver(post_save, sender='auth.user')
def create_usertoken(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        Token.objects.create(user=instance)
