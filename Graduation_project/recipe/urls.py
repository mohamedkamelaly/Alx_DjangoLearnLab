from django.urls import path
from . import views
from .views import RecipeListView, DetailListView,CreateListView, UpdateListView, DeleteListView

urlpatterns = [
    path('', RecipeListView.as_view(), name= 'recipe-home'),
    path('recipe/<int:pk>', DetailListView.as_view(), name= 'recipe-detail'),
    path('recipe/create/', CreateListView.as_view(), name= 'recipe-create'),
    path('recipe/<int:pk>/update', UpdateListView.as_view(), name= 'recipe-update'),
    path('recipe/<int:pk>/delete', DeleteListView.as_view(), name= 'recipe-delete'),
    path('about/', views.about, name= 'recipe-about'),

    
]
