from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from appfood.views import IndexView
# User related views
from appfood.views import RegisterView, RegisterTypeView
from django.contrib.auth.views import login, logout
from appfood.views import ProfileView, UsersSavedRecipesView
# Recipe related views
from appfood.views import AllRecipeView, GlutenFreeRecipeView, DairyFreeRecipeView, EggFreeRecipeView
from appfood.views import PeanutFreeRecipeView, SeafoodFreeRecipeView, SpecificRecipeView
from appfood.views import SoyFreeRecipeView
# User Recipe Interaction related views
from appfood.views import SaveRecipeView, DeleteBookmarkView, AddFoodView, EditFoodView, SearchRecipesView, CookFoodView, UpdateShoppingListView, AddItemsToShoppingListView
from appfood.views import ViewUserProfileView, UploadRecipeView, EditUploadedRecipeView, DeleteUploadedRecipeView, ViewUploadedRecipeView
from appfood.views import BookmarkUploadedRecipeView, DeleteBookmarkedUploadView

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
    url(r'^savedrecipes/(?P<username>[A-Za-z0-9_\-]+)', UsersSavedRecipesView.as_view(), name='userssavedrecipesview'),
    # User profile and recipe information
    url(r'^userprofiles/(?P<username>[A-Za-z0-9_\-]+)', ViewUserProfileView.as_view(), name='viewuserprofileview'),
    url(r'^uploadrecipe/$', UploadRecipeView.as_view(), name='uploadrecipeview'),
    url(r'^edituploadrecipe/(?P<recipe_id>\d+)/$', EditUploadedRecipeView.as_view(), name='edituseruploadedrecipe'),
    url(r'^deleteuploadrecipe/(?P<recipe_id>\d+)/$', DeleteUploadedRecipeView.as_view(), name='deletuploadedrecipeview'),
    url(r'^viewuploadedrecipe/(?P<recipe_id>\d+)/$', ViewUploadedRecipeView.as_view(), name='viewuploadededrecipeview'),
    url(r'^bookmarkuploadedrecipe/(?P<recipe_id>\d+)/$', BookmarkUploadedRecipeView.as_view(), name='bookmarkuploadedrecipeview'),
    url(r'^deletebookmarkedupload/(?P<recipe_id>\d+)/$', DeleteBookmarkedUploadView.as_view(), name='deletebookmarkeduploadview'),
    # Recipe related Views
    url(r'^recipes/allrecipes/(?P<page_count>[0-9_\-]+)/$', AllRecipeView.as_view(), name='allrecipeview'),
    url(r'^recipes/glutenfreerecipes/(?P<page_count>[0-9_\-]+)/$', GlutenFreeRecipeView.as_view(), name='glutenfreerecipeview'),
    url(r'^recipes/dairyfreerecipes/(?P<page_count>[0-9_\-]+)/$', DairyFreeRecipeView.as_view(), name='dairyfreerecipeview'),
    url(r'^recipes/eggfreerecipes/(?P<page_count>[0-9_\-]+)/$', EggFreeRecipeView.as_view(), name='eggfreerecipeview'),
    url(r'^recipes/peanutfreerecipes/(?P<page_count>[0-9_\-]+)/$', PeanutFreeRecipeView.as_view(), name='peanutfreerecipeview'),
    url(r'^recipes/seafoodfreerecipes/(?P<page_count>[0-9_\-]+)/$', SeafoodFreeRecipeView.as_view(), name='seafoodfreerecipeview'),
    url(r'^recipes/soyfreerecipes/(?P<page_count>[0-9_\-]+)/$', SoyFreeRecipeView.as_view(), name='soyfreerecipeview'),
    url(r'^recipes/specificrecipe/(?P<recipe_id>[A-Za-z0-9_\-]+)/$', SpecificRecipeView.as_view(), name='specificrecipeview'),
    # User Recipe Interactions
    url(r'^recipes/saverecipe/(?P<recipe_id>[A-Za-z0-9_\-]+)/$', SaveRecipeView.as_view(), name='saverecipeview'),
    url(r'^recipes/deleterecipe/(?P<recipe_id>[0-9_\-]+)/$', DeleteBookmarkView.as_view(), name='deletebookmarkview'),
    url(r'^recipes/searchrecipe/(?P<page_count>[0-9_\-]+)$', SearchRecipesView.as_view(), name='searchrecipesview'),
    url(r'^addfood/$', AddFoodView.as_view(), name='addfoodview'),
    url(r'^editfood/(?P<food_id>\d+)/$', EditFoodView.as_view(), name='editfoodview'),
    url(r'^cookfood/(?P<recipe_id>\d+)/$', CookFoodView.as_view(), name='cookfoodview'),
    url(r'^shoppinglist/$', UpdateShoppingListView.as_view(), name='updateshoppinglistview'),
    url(r'^shoppinglist/additems/(?P<recipe_id>\d+)/$', AddItemsToShoppingListView.as_view(), name='additemstoshoppinglistview'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
