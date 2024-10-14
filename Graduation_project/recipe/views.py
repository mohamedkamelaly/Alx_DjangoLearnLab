from django.shortcuts import render, HttpResponse
from .models import Recipe
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
# Create your views here.

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe/home.html'
    context_object_name= 'recipes'

class DetailListView(DetailView):
    model = Recipe

class CreateListView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdateListView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Recipe
    fields = ['title', 'description']
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class DeleteListView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe-home')
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    
def about(request):
    return render(request,"recipe/about.html", {'title' : 'About Us Page '})
    