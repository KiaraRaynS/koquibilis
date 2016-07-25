from django.contrib import admin
from appfood.models import Recipe, UserPage

# Register your models here.


class UserPageAdmin(admin.ModelAdmin):
    list_display = ['user']
admin.site.register(UserPage, UserPageAdmin)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title']
admin.site.register(Recipe, RecipeAdmin)