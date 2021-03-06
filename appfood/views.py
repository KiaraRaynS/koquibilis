from django.shortcuts import render, render_to_response
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse_lazy
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
# Oauth Views
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
# Models
from appfood.models import Recipe, UserPage, SavedRecipe, FoodItem, ShoppingList, UserUploadedRecipe, UploadedRecipeBookmark
import requests
# Views
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, View
# User forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Keys and API Data
import os


# Oauth Class
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, OAuth2!")


def home(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})
    return render_to_response('appfood/home.html',
                              context_instance=context)


class IndexView(TemplateView):
    template_name = 'indexview.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            userpage = UserPage.objects.get(user=user)
            bookmarks = SavedRecipe.objects.filter(user=user.id).order_by('-bookmark_date')
            bookmarks = bookmarks[:10]
            userinventory = FoodItem.objects.filter(user=user.id).order_by('-last_edit')
            shoppinglist = ShoppingList.objects.get(user=user)
            if shoppinglist.ingredients:
                shoppinglist_length = len(shoppinglist.ingredients)
            else:
                shoppinglist_length = 0
            uploaded_recipes = UserUploadedRecipe.objects.filter(user=user)
            bookmarked_uploads = UploadedRecipeBookmark.objects.filter(user=user).order_by('-bookmark_date')
            # Get user food list
            userinventory_list = []
            for item in userinventory:
                if item.quantity > 0:
                    userinventory_list.append(item.name.replace(' ', '').lower())
            # Bookmarked food list
            possible_recipes_frombookmarks = []
            for recipe in bookmarks:
                recipe_ingredients = recipe.ingredients.replace('[', '')
                recipe_ingredients = recipe_ingredients.replace(']', '')
                recipe_ingredients = recipe_ingredients.replace(' ', '')
                recipe_ingredients = recipe_ingredients.replace("'", '')
                recipe_ingredients_list = recipe_ingredients.split(',')
                if set(recipe_ingredients_list) <= set(userinventory_list):
                    possible_recipes_frombookmarks.append(recipe)
            possible_recipes_fromuploads = []
            for recipe in uploaded_recipes:
                recipe_ingredients = recipe.basic_ingredients.replace('[', '')
                recipe_ingredients = recipe_ingredients.replace(']', '')
                recipe_ingredients = recipe_ingredients.replace(' ', '')
                recipe_ingredients = recipe_ingredients.replace("'", '')
                recipe_ingredients_l = recipe_ingredients.split(',')
                recipe_ingredients_list = []
                for item in recipe_ingredients_l:
                    if item != '':
                        recipe_ingredients_list.append(item)
                if set(recipe_ingredients_list) <= set(userinventory_list):
                    possible_recipes_fromuploads.append(recipe)
            possible_recipes_count = len(possible_recipes_frombookmarks) + len(possible_recipes_fromuploads)
            context = {
                    'userpage': userpage,
                    'bookmarks': bookmarks,
                    'useritems': userinventory,
                    'possible_recipes': possible_recipes_frombookmarks,
                    'possible_uploadedrecipes': possible_recipes_fromuploads,
                    'possible_recipes_count': possible_recipes_count,
                    'shoppinglist': shoppinglist,
                    'shoppinglist_length': shoppinglist_length,
                    'uploaded_recipes': uploaded_recipes,
                    'bookmarked_uploads': bookmarked_uploads,
                    }
            return context


# User Registration
class RegisterTypeView(TemplateView):
    template_name = 'registertypeview.html'


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = '/'


class ProfileView(UpdateView):
    template_name = 'profileview.html'
    model = UserPage
    fields = ['photo', 'description', 'bookmarks_private', 'uploads_private']
    success_url = reverse_lazy('profileview')
    authentication_classes = (authentication.TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        user = self.request.user
        if user.is_authenticated():
            return UserPage.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        holdphoto = os.environ['DEFAULT_ICON_DIR']
        # holdphoto = "https://s3.amazonaws.com/koquibilis-profilephotos/default.png"
        if user.is_authenticated():
            context['userdata'] = UserPage.objects.get(user=user)
            context['holderphoto'] = holdphoto
        return context


# User Profile
class ViewUserProfileView(TemplateView):
    template_name = 'userprofileview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        current_user = self.request.user
        userpage = UserPage.objects.get(user=user)
        uploads = UserUploadedRecipe.objects.filter(user=user).order_by('-upload_date')
        uploads = uploads[:5]
        bookmarked_recipes = SavedRecipe.objects.filter(user=user).order_by('-bookmark_date')
        bookmarked_recipes = bookmarked_recipes[:5]
        context['user'] = user
        context['current_user'] = current_user
        context['userpage'] = userpage
        context['uploads'] = uploads
        context['bookmarked_recipes'] = bookmarked_recipes
        return context


# User Uploaded Recipes Interactions
class UsersSavedRecipesView(ListView):
    model = SavedRecipe
    template_name = 'userssavedrecipesview.html'
    paginate_by = 10
    context_object_name = 'recipes'

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        saved_recipes = SavedRecipe.objects.filter(user=user).order_by('-bookmark_date')
        return saved_recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        context['current_user'] = current_user
        context['user'] = user
        return context


class UsersUploadedRecipesView(ListView):
    template_name = 'usersuploadedrecipesview.html'
    model = UserUploadedRecipe
    paginate_by = 10
    context_object_name = 'recipes'

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        user_uploads = UserUploadedRecipe.objects.filter(user=user).order_by('-upload_date')
        return user_uploads

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        current_user = self.request.user
        context['user'] = user
        context['current_user'] = current_user
        return context


class SearchUploadedRecipesView(TemplateView):
    template_name = 'searchuploadedrecipesview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "GET":
            search_query = self.request.GET.get('search_box', None)
            search_list = search_query.split(' ')
            user_id = self.kwargs['user_id']
            user = User.objects.get(id=user_id)
            user_uploads = UserUploadedRecipe.objects.filter(user=user)
            matches = []
            for upload in user_uploads:
                title_words = upload.title.split(' ')
                notes_words = upload.uploader_notes.split(' ')
                if set(search_list) <= set(title_words):
                    matches.append(upload)
                if set(search_list) <= set(notes_words):
                    matches.append(upload)
            print(matches)
            context['search'] = search_query
            context['matches'] = matches
        return context


# Recipe related views
class AllRecipeView(ListView):
    model = Recipe
    template_name = 'allrecipesview.html'

    def get_context_data(self, **kwargs):
        api_auth = os.environ['API_AUTH']
        base_url = 'http://api.yummly.com/v1/api/recipes?'
        recipes_list_url = base_url + api_auth
        recipe_count = self.kwargs['page_count']
        previous_page = int(recipe_count) - 10
        next_page = int(recipe_count) + 10
        pagination = '&maxResult=10&start=' + str(recipe_count)
        # All Recipes
        all_recipes_url = recipes_list_url + pagination
        allrecipe_results = requests.get(all_recipes_url).json()
        allrecipe = allrecipe_results['matches']
        # context
        context = {
                'allrecipes': allrecipe,
                'previous_page': previous_page,
                'next_page': next_page,
                'current_page': recipe_count,
                }
        return context


class GlutenFreeRecipeView(ListView):
    model = Recipe
    template_name = 'glutenfreerecipeview.html'

    def get_context_data(self, **kwargs):
        api_auth = os.environ['API_AUTH']
        base_url = 'http://api.yummly.com/v1/api/recipes?'
        recipes_list_url = base_url + api_auth
        recipe_count = self.kwargs['page_count']
        previous_page = int(recipe_count) - 10
        next_page = int(recipe_count) + 10
        pagination = '&maxResult=10&start=' + str(recipe_count)
        glutenfree_url = recipes_list_url + '&allowedAllergy[]=393^Gluten-Free' + pagination
        glutenfree_results = requests.get(glutenfree_url).json()
        glutenfree = glutenfree_results['matches']
        context = {
                'previous_page': previous_page,
                'next_page': next_page,
                'current_page': recipe_count,
                'recipes': glutenfree
                }
        return context


class DairyFreeRecipeView(TemplateView):
    template_name = 'dairyfreerecipeview.html'

    def get_context_data(self, **kwargs):
        api_auth = os.environ['API_AUTH']
        base_url = 'http://api.yummly.com/v1/api/recipes?'
        recipes_list_url = base_url + api_auth
        recipe_count = self.kwargs['page_count']
        previous_page = int(recipe_count) - 10
        next_page = int(recipe_count) + 10
        pagination = '&maxResult=10&start=' + str(recipe_count)
        dairyfree_url = recipes_list_url + '&allowedAllergy[]=396^Dairy-Free' + pagination
        dairyfree_results = requests.get(dairyfree_url).json()
        dairyfree = dairyfree_results['matches']
        context = {
                'previous_page': previous_page,
                'next_page': next_page,
                'current_page': recipe_count,
                'recipes': dairyfree,
                }
        return context


class EggFreeRecipeView(TemplateView):
    template_name = 'eggfreerecipeview.html'

    def get_context_data(self, **kwargs):
        api_auth = os.environ['API_AUTH']
        base_url = 'http://api.yummly.com/v1/api/recipes?'
        recipes_list_url = base_url + api_auth
        recipe_count = self.kwargs['page_count']
        previous_page = int(recipe_count) - 10
        next_page = int(recipe_count) + 10
        pagination = '&maxResult=10&start=' + str(recipe_count)
        eggfree_url = recipes_list_url + '&allowedAllergy[]=397^Egg-Free' + pagination
        eggfree_results = requests.get(eggfree_url).json()
        eggfree = eggfree_results['matches']
        context = {
                'previous_page': previous_page,
                'next_page': next_page,
                'current_page': recipe_count,
                'recipes': eggfree,
                }
        return context


class PeanutFreeRecipeView(TemplateView):
    template_name = 'peanutfreerecipeview.html'

    def get_context_data(self, **kwargs):
        api_auth = os.environ['API_AUTH']
        base_url = 'http://api.yummly.com/v1/api/recipes?'
        recipes_list_url = base_url + api_auth
        recipe_count = self.kwargs['page_count']
        previous_page = int(recipe_count) - 10
        next_page = int(recipe_count) + 10
        pagination = '&maxResult=10&start=' + str(recipe_count)
        peanutfree_url = recipes_list_url + '&allowedAllergy[]=394^Peanut-Free' + pagination
        peanutfree_results = requests.get(peanutfree_url).json()
        peanutfree = peanutfree_results['matches']
        context = {
                'previous_page': previous_page,
                'next_page': next_page,
                'current_page': recipe_count,
                'recipes': peanutfree,
                }
        return context


class SeafoodFreeRecipeView(TemplateView):
    template_name = 'seafoodfreerecipeview.html'

    def get_context_data(self, **kwargs):
        api_auth = os.environ['API_AUTH']
        base_url = 'http://api.yummly.com/v1/api/recipes?'
        recipes_list_url = base_url + api_auth
        recipe_count = self.kwargs['page_count']
        previous_page = int(recipe_count) - 10
        next_page = int(recipe_count) + 10
        pagination = '&maxResult=10&start=' + str(recipe_count)
        seafoodfree_url = recipes_list_url + '&allowedAllergy[]=398^Seafood-Free' + pagination
        seafoodfree_results = requests.get(seafoodfree_url).json()
        seafoodfree = seafoodfree_results['matches']
        context = {
                'previous_page': previous_page,
                'next_page': next_page,
                'current_page': recipe_count,
                'recipes': seafoodfree,
                }
        return context


class SoyFreeRecipeView(TemplateView):
    template_name = 'soyfreerecipeview.html'

    def get_context_data(self, **kwargs):
        api_auth = os.environ['API_AUTH']
        base_url = 'http://api.yummly.com/v1/api/recipes?'
        recipes_list_url = base_url + api_auth
        recipe_count = self.kwargs['page_count']
        previous_page = int(recipe_count) - 10
        next_page = int(recipe_count) + 10
        pagination = '&maxResult=10&start=' + str(recipe_count)
        soyfoodfree_url = recipes_list_url + '&allowedAllergy[]=399^Seafood-Free' + pagination
        soyfoodfree_results = requests.get(soyfoodfree_url).json()
        soyfoodfree = soyfoodfree_results['matches']
        context = {
                'previous_page': previous_page,
                'next_page': next_page,
                'current_page': recipe_count,
                'recipes': soyfoodfree,
                }
        return context


class SpecificRecipeView(TemplateView):
    template_name = 'specificrecipeview.html'

    def get_context_data(self, **kwargs):
        api_auth = os.environ['API_AUTH']
        base_url = 'http://api.yummly.com/v1/api/recipe/'
        context = super().get_context_data(**kwargs)
        recipe_id = self.kwargs['recipe_id']
        recipe_url = base_url + recipe_id + "?" + api_auth
        recipe_results = requests.get(recipe_url).json()
        recipe_images = recipe_results['images']
        recipe_images_dict = recipe_images[0]
        urlsbysize = recipe_images_dict['imageUrlsBySize']
        image_link = urlsbysize['360']
        context = {
                'recipedata': recipe_results,
                'image_url': image_link,
                }
        return context


# User and Recipe Interaction Views
class SaveRecipeView(CreateView):
    template_name = 'saverecipeview.html'
    model = SavedRecipe
    fields = ['note']
    success_url = '/'
    authentication_classes = (authentication.TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_context_data(self, **kwargs):
        api_auth = os.environ['API_AUTH']
        base_url = 'http://api.yummly.com/v1/api/recipe/'
        context = super().get_context_data(**kwargs)
        recipe_id = self.kwargs['recipe_id']
        recipe_url = base_url + recipe_id + "?" + api_auth
        recipe_results = requests.get(recipe_url).json()
        context['recipe'] = recipe_results
        # To get recipe image
        recipe_images = recipe_results['images']
        recipe_img_dict = recipe_images[0]
        urlsbysize = recipe_img_dict['imageUrlsBySize']
        recipeimage = urlsbysize['90']
        # Return context
        context['recipeimage'] = recipeimage
        return context

    def form_valid(self, form):
        api_auth = os.environ['API_AUTH']
        base_url = 'http://api.yummly.com/v1/api/recipe/'
        recipe_id = self.kwargs['recipe_id']
        recipe_url = base_url + recipe_id + "?" + api_auth
        recipe_results = requests.get(recipe_url).json()
        recipe_title = recipe_results['name']
        detailed_ingredients = recipe_results['ingredientLines']
        # Recipe Ingredients
        recipetitle_list = recipe_title.split(' ')
        recipei_baseurl = 'http://api.yummly.com/v1/api/recipes?' + api_auth + "&q="
        getingredientsurl = recipei_baseurl
        for item in recipetitle_list:
            if item != " ":
                getingredientsurl += item + '+'
        reciperesults = requests.get(getingredientsurl).json()
        recipematches = reciperesults['matches']
        for item in recipematches:
            if item['id'] == recipe_id:
                recipeingredients = item['ingredients']
        # Image urls
        recipe_images = recipe_results['images']
        recipe_images_dict = recipe_images[0]
        urlsbysize = recipe_images_dict['imageUrlsBySize']
        image_large = urlsbysize['360']
        image_small = urlsbysize['90']
        # Form saves
        form.instance.title = recipe_title
        form.instance.recipe_key = recipe_id
        form.instance.ingredients = recipeingredients
        form.instance.user_id = self.request.user.id
        form.instance.big_image = image_large
        form.instance.small_image = image_small
        form.instance.detailed_ingredients = detailed_ingredients
        return super(SaveRecipeView, self).form_valid(form)


class SearchRecipesView(TemplateView):
    template_name = 'searchrecipesview.html'
    base_url = 'http://api.yummly.com/v1/api/recipes?'
    api_key = os.environ['API_AUTH']
    f_url = base_url + api_key + "&"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_url = 'http://api.yummly.com/v1/api/recipes?'
        api_key = os.environ['API_AUTH']
        base_url = api_url + api_key + "&q="
        # Get search url
        if self.request.method == "GET":
            search_query = self.request.GET.get('search_box', None)
            search_list = search_query.split(' ')
        new_url = base_url
        search_string = ''
        for item in search_list:
            search_string += item + '+'
        search_box = '?search_box=' + search_string[:-1]
        for item in search_list:
            if item != ' ':
                new_url += item + '+'
        recipe_count = self.kwargs['page_count']
        previous_page = str(int(recipe_count) - 10)
        next_page = int(recipe_count) + 10
        pagination = '&maxResult=10&start=' + str(recipe_count)
        final_url = new_url + pagination
        # Make api call for search
        search_requests = requests.get(final_url).json()
        search_results = search_requests['matches']
        context['results'] = search_results
        context['search_box'] = search_box
        context['previous'] = previous_page
        context['next'] = next_page
        context['current_page'] = str(recipe_count)
        return context


# User Bookmark Actions
class DeleteBookmarkView(DeleteView):
    template_name = 'deletebookmarkview.html'
    success_url = '/'

    def get_object(self, queryset=None):
        object_key = self.kwargs['recipe_id']
        return SavedRecipe.objects.get(id=object_key)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['current_user'] = current_user
        return context

# Inventory handling


class AddFoodView(CreateView):
    model = FoodItem
    fields = ['name', 'measurementunit', 'quantity']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddFoodView, self).form_valid(form)


class EditFoodView(UpdateView):
    model = FoodItem
    template_name = 'editfoodview.html'
    fields = ['quantity']
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        food_id = self.kwargs['food_id']
        food_item = FoodItem.objects.get(id=food_id)
        context['current_user'] = current_user
        context['food_item'] = food_item
        return context

    def get_object(self, queryset=None):
        food_item = self.kwargs['food_id']
        return FoodItem.objects.get(id=food_item)

    def form_valid(self, form):
        form.instance.last_edit = timezone.now()
        return super(EditFoodView, self).form_valid(form)


class CookFoodView(View):

    def post(self, request, *args, **kwargs):
        context = {}
        data = self.request.POST
        for value in data.items():
            if value[0] != "csrfmiddlewaretoken":
                recipeitem_id = value[0]
                update_item = FoodItem.objects.get(id=recipeitem_id)
                recipe_quantity = int(value[1])
                if recipe_quantity < 0:
                    recipe_quantity = 0
                update_item.quantity = recipe_quantity
                update_item.save()
        return HttpResponseRedirect('/')
        return render(request, "cookfoodview.html", context)

    def get(self, request, recipe_id):
        context = {}
        user = self.request.user
        if user.is_authenticated():
            recipe = self.kwargs['recipe_id']
            recipe_to_cook = SavedRecipe.objects.get(id=recipe)
            useringredients = FoodItem.objects.filter(user=user, quantity__gt=0)
            # Get Ingredients to edit
            ingredients_in_recipe = []
            for item in useringredients:
                if item.name in recipe_to_cook.ingredients:
                    ingredients_in_recipe.append(item)
            # Make clean list of recipe detailed ingredients
            detailedingredients_text = recipe_to_cook.detailed_ingredients
            cleaned_text = detailedingredients_text.replace('[', '')
            cleaned_text = cleaned_text.replace(']', '')
            cleaned_text = cleaned_text.replace("'", '')
            recipe_detailed_ingredients = cleaned_text.split(',')
            # Return context
            context['ingredientsbeingused'] = ingredients_in_recipe
            context['recipe'] = recipe_to_cook
            context['detailedingredients'] = recipe_detailed_ingredients
            return render(request, "cookfoodview.html", context)
        else:
            return render(request, "cookfoodview.html", context)


class CookUploadedFoodView(View):

    def post(self, request, *args, **kwargs):
        context = {}
        data = self.request.POST
        for value in data.items():
            if value[0] != "csrfmiddlewaretoken":
                recipeitem_id = value[0]
                update_item = FoodItem.objects.get(id=recipeitem_id)
                recipe_quantity = int(value[1])
                if recipe_quantity < 0:
                    recipe_quantity = 0
                update_item.quantity = recipe_quantity
                update_item.save()
        return HttpResponseRedirect('/')
        return render(request, "cookuploadedfoodview.html", context)

    def get(self, request, recipe_id):
        context = {}
        user = self.request.user
        if user.is_authenticated():
            recipe = self.kwargs['recipe_id']
            recipe_to_cook = UserUploadedRecipe.objects.get(id=recipe)
            useringredients = FoodItem.objects.filter(user=user, quantity__gt=0)
            # Get Ingredients to edit
            ingredients_in_recipe = []
            for item in useringredients:
                if item.name in recipe_to_cook.basic_ingredients:
                    ingredients_in_recipe.append(item)
            # Make clean list of recipe detailed ingredients
            detailedingredients_text = recipe_to_cook.detailed_ingredients
            cleaned_text = detailedingredients_text.replace('[', '')
            cleaned_text = cleaned_text.replace(']', '')
            cleaned_text = cleaned_text.replace("'", '')
            recipe_detailed_ingredients = cleaned_text.split(',')
            # Return context
            context['ingredientsbeingused'] = ingredients_in_recipe
            context['ingredientslength'] = len(detailedingredients_text)
            context['recipe'] = recipe_to_cook
            context['detailedingredients'] = recipe_detailed_ingredients
            return render(request, "cookuploadedfoodview.html", context)
        else:
            return render(request, "cookuploadedfoodview.html", context)


class CookFoodViewx(UpdateView):
    model = FoodItem
    template_name = 'cookfoodview.html'
    fields = ['quantity']
    success_url = '/'

    def get_object(self, queryset=None):
        recipe = self.kwargs['recipe_id']
        recipe_obj = SavedRecipe.objects.get(id=recipe)
        return recipe_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        recipe = self.kwargs['recipe_id']
        recipe_to_cook = SavedRecipe.objects.get(id=recipe)
        useringredients = FoodItem.objects.filter(user=user)
        # Get Ingredients to edit
        ingredients_in_recipe = []
        for item in useringredients:
            if item.name in recipe_to_cook.ingredients:
                ingredients_in_recipe.append(item)
        # Make clean list of recipe detailed ingredients
        detailedingredients_text = recipe_to_cook.detailed_ingredients
        cleaned_text = detailedingredients_text.replace('[', '')
        cleaned_text = cleaned_text.replace(']', '')
        cleaned_text = cleaned_text.replace("'", '')
        recipe_detailed_ingredients = cleaned_text.split(',')
        # Return context
        context['ingredientsbeingused'] = ingredients_in_recipe
        context['recipe'] = recipe_to_cook
        context['detailedingredients'] = recipe_detailed_ingredients
        return context


# Shopping List Views
class UpdateShoppingListView(UpdateView):
    model = ShoppingList
    fields = ['ingredients']
    template_name = 'updateshoppinglistview.html'
    success_url = '/'

    def get_object(self, queryset=None):
        user = self.request.user
        if user.is_authenticated():
            return ShoppingList.objects.get(user=user)


class AddItemsToShoppingListView(UpdateView):
    model = ShoppingList
    fields = []
    template_name = 'additemstoshoppinglistview.html'
    success_url = '/'

    def get_object(self, queryset=None):
        user = self.request.user
        shopping_list = ShoppingList.objects.get(user=user)
        return shopping_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        shopping_list = ShoppingList.objects.get(user=user)
        recipe_id = self.kwargs['recipe_id']
        recipe = SavedRecipe.objects.get(id=recipe_id)
        # Get list ingredients
        recipeingredients_str = recipe.detailed_ingredients
        ingredients = recipeingredients_str.replace("'", '')
        ingredients = ingredients.replace('[', '')
        ingredients = ingredients.replace(']', '')
        ingredients_list = ingredients.split(',')
        # Get
        context['shoppinglist'] = shopping_list
        context['ingredients'] = ingredients_list
        context['recipe'] = recipe
        return context

    def form_valid(self, form):
        user = self.request.user
        shopping_list = ShoppingList.objects.get(user=user)
        current_list = shopping_list.ingredients
        # Get Ingredients List
        recipe_id = self.kwargs['recipe_id']
        recipe = SavedRecipe.objects.get(id=recipe_id)
        recipeingredients_str = recipe.detailed_ingredients
        ingredients = recipeingredients_str.replace("'", '')
        ingredients = ingredients.replace('[', '')
        ingredients = ingredients.replace(']', '')
        ingredients_list = ingredients.split(',')
        if current_list is None:
            new_list = ''
        else:
            new_list = current_list + ', '
        for item in ingredients_list:
            new_list = new_list + item + ','
        form.instance.ingredients = new_list
        return super().form_valid(form)


class ClearShoppingListView(UpdateView):
    model = ShoppingList
    template_name = 'clearshoppinglistview.html'
    fields = []
    context_object_name = 'shopping_list'
    success_url = '/'

    def get_object(self, queryset=None):
        user = self.request.user
        if user.is_authenticated():
            shoppinglist = ShoppingList.objects.get(user=user)
            return shoppinglist

    def form_valid(self, form):
        form.instance.ingredients = ''
        return super().form_valid(form)


# User Created Recipe Views
class UploadRecipeView(CreateView):
    model = UserUploadedRecipe
    success_url = '/'
    fields = ['title', 'basic_ingredients', 'detailed_ingredients', 'uploader_notes', 'instructions', 'recipephoto', 'recipe_link']

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(UploadRecipeView, self).form_valid(form)


class EditUploadedRecipeView(UpdateView):
    model = UserUploadedRecipe
    success_url = '/'
    template_name = 'edituploadedrecipeview.html'
    fields = ['title', 'basic_ingredients', 'detailed_ingredients', 'uploader_notes', 'instructions', 'recipephoto']

    def get_object(self, queryset=None):
        recipe_id = self.kwargs['recipe_id']
        return UserUploadedRecipe.objects.get(id=recipe_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        recipe_id = self.kwargs['recipe_id']
        recipe_data = UserUploadedRecipe.objects.get(id=recipe_id)
        context['recipe_data'] = recipe_data
        context['currentuser'] = current_user
        return context


class DeleteUploadedRecipeView(DeleteView):
    model = UserUploadedRecipe
    success_url = '/'

    def get_object(self, queryset=None):
        recipe_id = self.kwargs['recipe_id']
        return UserUploadedRecipe.objects.get(id=recipe_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_id = self.kwargs['recipe_id']
        user = self.request.user
        context['recipe'] = UserUploadedRecipe.objects.get(id=recipe_id)
        context['currentuser'] = user
        return context


class ViewUploadedRecipeView(TemplateView):
    template_name = 'viewuploadedrecipeview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_id = self.kwargs['recipe_id']
        user = self.request.user
        recipe = UserUploadedRecipe.objects.get(id=recipe_id)
        context['recipe'] = recipe
        context['currentuser'] = user
        return context


class BookmarkUploadedRecipeView(CreateView):
    model = UploadedRecipeBookmark
    fields = ['bookmark_notes']
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_id = self.kwargs['recipe_id']
        recipe = UserUploadedRecipe.objects.get(id=recipe_id)
        context['recipe'] = recipe
        return context

    def form_valid(self, form):
        recipe_id = self.kwargs['recipe_id']
        user = self.request.user
        recipe = UserUploadedRecipe.objects.get(id=recipe_id)
        form.instance.uploader = recipe.user
        form.instance.user = user
        form.instance.recipe = recipe
        form.instance.title = recipe.title
        return super(BookmarkUploadedRecipeView, self).form_valid(form)


class DeleteBookmarkedUploadView(DeleteView):
    model = UploadedRecipeBookmark
    success_url = '/'

    def get_object(self, queryset=None):
        recipe_id = self.kwargs['recipe_id']
        return UploadedRecipeBookmark.objects.get(id=recipe_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_id = self.kwargs['recipe_id']
        recipe = UploadedRecipeBookmark.objects.get(id=recipe_id)
        context['recipe'] = recipe
        return context
