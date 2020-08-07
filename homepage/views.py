from django.shortcuts import render
from homepage.models import Recipe, Author
# Create your views here.
def index(request):
    all_recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': all_recipes})

def recipe_detail(request, recipe_id):
    this_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, 'recipe_detail.html', {'recipe': this_recipe })

def author_details(request, author_id):
    authors_recipes = Recipe.objects.filter(author=Author.objects.get(id=author_id))
    this_author = Author.objects.filter(id=author_id).first()
    return render(request, 'author_detail.html', { 'author': this_author, "recipes": authors_recipes})