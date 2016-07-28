from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.core.urlresolvers import reverse_lazy
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
# Oauth Views
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
# Models
from appfood.models import Recipe, UserPage, SavedRecipe, FoodItem
# Scraping
from bs4 import BeautifulSoup
import requests
# Views
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
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
            userinventory = FoodItem.objects.filter(user=user.id).order_by('-date_added')
            # Get user food list
            userinventory_list = []
            for item in userinventory:
                if item.quantity > 0:
                    userinventory_list.append(item.name)
            possible_recipes = []
            for recipe in bookmarks:
                # print(recipe.ingredients)
                if all(recipe.ingredients) in userinventory_list:
                    possible_recipes.append(recipe)
            # print(possible_recipes)
            context = {
                    'userpage': userpage,
                    'bookmarks': bookmarks,
                    'useritems': userinventory,
                    'possible_recipes': possible_recipes,
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
    fields = ['userhandle', 'photo', 'description']
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
        if user.is_authenticated():
            context['userdata'] = UserPage.objects.get(user=user)
        return context


class RecipeView(ListView):
    model = Recipe

    def get_context_data(self, **kwargs):
        api_auth = os.environ['API_AUTH']
        base_url = 'http://api.yummly.com/v1/api/recipes?'
        recipes_list_url = base_url + api_auth
        # All Recipes
        allrecipe_results = requests.get(recipes_list_url).json()
        allrecipe = allrecipe_results['matches']
        # By allergens
        # Glutten
        gluttenfree_url = recipes_list_url + '&allowedAllergy[]=393^Gluten-Free'
        gluttenfree_results = requests.get(gluttenfree_url).json()
        gluttenfree = gluttenfree_results['matches']
        # Lactose
        dairyfree_url = recipes_list_url + "&allowedAllergy[]=393^Dairy-Free"
        dairyfree_results = requests.get(dairyfree_url).json()
        dairyfree = dairyfree_results['matches']
        # Egg
        eggfree_url = recipes_list_url + "&allowedAllergy[]=393^Egg-Free"
        eggfree_results = requests.get(eggfree_url).json()
        eggfree = eggfree_results['matches']
        # Peanut
        peanutfree_url = recipes_list_url + "&allowedAllergy[]=393^Peanut-Free"
        peanutfree_results = requests.get(peanutfree_url).json()
        peanutfree = peanutfree_results['matches']
        # Seafood
        seafoodfree_url = recipes_list_url + "&allowedAllergy[]&=393^Seafood-Free"
        seafoodfree_results = requests.get(seafoodfree_url).json()
        seafoodfree = seafoodfree_results['matches']
        # Soy
        soyfree_url = recipes_list_url + "&allowedAllergy[]&=393^Soy-Free"
        soyfree_results = requests.get(soyfree_url).json()
        soyfree = soyfree_results['matches']
        # context
        context = {
                'allrecipes': allrecipe,
                'gluttenfree': gluttenfree,
                'dairyfree': dairyfree,
                'eggfree': eggfree,
                'peanutfree': peanutfree,
                'seafoodfree': seafoodfree,
                'soyfree': soyfree,
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
        # recipe_ingredients = recipe_results['ingredientLines']
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
                print(item['recipeName'])
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
        for item in search_list:
            if item != ' ':
                new_url += item + '+'
        # Make api call for search
        search_requests = requests.get(new_url).json()
        search_results = search_requests['matches']
        context['results'] = search_results
        return context


class DeleteBookmarkView(DeleteView):
    template_name = 'deletebookmarkview.html'
    success_url = '/'

    def get_object(self, queryset=None):
        object_key = self.kwargs['recipe_id']
        return SavedRecipe.objects.get(id=object_key)

# Inventory handling


class AddFoodView(CreateView):
    model = FoodItem
    fields = ['name', 'quantity']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddFoodView, self).form_valid(form)


class EditFoodView(UpdateView):
    model = FoodItem
    template_name = 'editfoodview.html'
    fields = ['quantity']
    success_url = '/'

    def get_object(self, queryset=None):
        food_item = self.kwargs['food_id']
        return FoodItem.objects.get(id=food_item)


# For scraping recipes [Possibly discarded]
def get_recipe_data(request):
    content = requests.get('http://www.food.com/recipe/pancakes-25690').text
    contentsoup = BeautifulSoup(content, 'html.parser')
    recipepage = contentsoup.find(class_='fd-page-feed')
    for tag in recipepage.findAll('a', href=True):
        recipename = str(recipepage.find(class_='fd-recipe-title').text)
        ingredientsli = recipepage.find_all(class_='ingredient-data')
        instructions = str(contentsoup.find(class_='expanded'))
    context = {
            'recipename': recipename,
            'ingredientslist': ingredientsli,
            'instructions': instructions,
            }
    return render(request, 'indexview.html', context)
