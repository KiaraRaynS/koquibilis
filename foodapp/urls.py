from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from appfood.views import IndexView
# User related views
from appfood.views import RegisterView, RegisterTypeView
from django.contrib.auth.views import login, logout
from appfood.views import ProfileView
# Recipe related views
from appfood.views import RecipeView, SpecificRecipeView
# User Recipe Interaction related views
from appfood.views import SaveRecipeView, DeleteBookmarkView, AddFoodView, EditFoodView, SearchRecipesView, CookFoodView, UpdateShoppingListView, AddItemsToShoppingListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='indexview'),
    # User Status related Views
    url(r'^registertype/$', RegisterTypeView.as_view(), name='registertypeview'),
    url(r'^register/$', RegisterView.as_view(), name='registerview'),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profileview'),
    # Recipe related Views
    url(r'^recipes/$', RecipeView.as_view(), name='recipeview'),
    url(r'^recipes/specificrecipe/(?P<recipe_id>[A-Za-z0-9_\-]+)/$', SpecificRecipeView.as_view(), name='specificrecipeview'),
    # User Recipe Interactions
    url(r'^recipes/saverecipe/(?P<recipe_id>[A-Za-z0-9_\-]+)/$', SaveRecipeView.as_view(), name='saverecipeview'),
    url(r'^recipes/deleterecipe/(?P<recipe_id>[0-9_\-]+)/$', DeleteBookmarkView.as_view(), name='deletebookmarkview'),
    url(r'^recipes/searchrecipe/$', SearchRecipesView.as_view(), name='searchrecipesview'),
    url(r'^addfood/$', AddFoodView.as_view(), name='addfoodview'),
    url(r'^editfood/(?P<food_id>\d+)/$', EditFoodView.as_view(), name='editfoodview'),
    url(r'^cookfood/(?P<recipe_id>\d+)/$', CookFoodView.as_view(), name='cookfoodview'),
    url(r'^shoppinglist/$', UpdateShoppingListView.as_view(), name='updateshoppinglistview'),
    url(r'^shoppinglist/additems/(?P<recipe_id>\d+)/$', AddItemsToShoppingListView.as_view(), name='additemstoshoppinglistview'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
