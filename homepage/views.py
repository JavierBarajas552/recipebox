from django.shortcuts import render, HttpResponseRedirect, reverse
from homepage.models import Recipe, Author
from homepage.forms import AddRecipeForm, AddAuthorForm
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


def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                time_required = data.get('time_required'),
                description = data.get('description'),
                instruction = data.get('instruction'),
                author = data.get('author'))
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = AddRecipeForm()
        return render(request, "add_recipe.html", {'form' : form})

def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data.get('name'),
                bio = data.get('bio'))
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = AddAuthorForm()
        return render(request, "add_author.html", {'form' : form})
