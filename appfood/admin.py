from django.contrib import admin
from appfood.models import Recipe, UserPage, SavedRecipe, ShoppingList, UserUploadedRecipe, UploadedRecipeBookmark

# Register your models here.


class UserPageAdmin(admin.ModelAdmin):
    list_display = ['user']
admin.site.register(UserPage, UserPageAdmin)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title']
admin.site.register(Recipe, RecipeAdmin)


class SavedRecipeAdmin(admin.ModelAdmin):
    list_display = ['title']
admin.site.register(SavedRecipe, SavedRecipeAdmin)


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['user']
admin.site.register(ShoppingList, ShoppingListAdmin)


class UserUploadedRecipeAdmin(admin.ModelAdmin):
    list_display = ['user', 'title']
admin.site.register(UserUploadedRecipe, UserUploadedRecipeAdmin)


class UploadedRecipeBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']
admin.site.register(UploadedRecipeBookmark, UploadedRecipeBookmarkAdmin)
