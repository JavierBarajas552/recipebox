from django.shortcuts import render, HttpResponseRedirect, reverse
from homepage.models import Recipe, Author, Favorites
from homepage.forms import AddRecipeForm, AddAuthorForm, LoginForm, EditRecipeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User


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
    favorites = Favorites.objects.filter(author=this_author)
    return render(request, 'author_detail.html', { 'author': this_author, "recipes": authors_recipes, 'favorites': favorites })



@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data.get('author') == None:
                data['author'] = request.user.author
            Recipe.objects.create(
                title=data.get('title'),
                time_required=data.get('time_required'),
                description=data.get('description'),
                instruction=data.get('instruction'),
                author=data.get('author'))
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = AddRecipeForm()
        if not request.user.is_staff:
            del form.fields['author']
        return render(request, "generic_form.html", {'form': form})


@staff_member_required
def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data.get('name'),
                bio=data.get('bio'),
                user=User.objects.create_user(username=data.get('username'), password=data.get('password'))
            )
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = AddAuthorForm()
        return render(request, "generic_form.html", {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get('username'), password=data.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('homepage')))
    form = LoginForm()
    return render(request, "generic_form.html", {'form' : form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def edit_view(request, recipe_id):
    this_recipe = Recipe.objects.filter(id=recipe_id).first()
    if request.method == "POST":
        form = EditRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            this_recipe.title = data["title"]
            this_recipe.time_required = data["time_required"]
            this_recipe.description = data["description"]
            this_recipe.instruction = data["instruction"]
            this_recipe.author = data["author"]
            this_recipe.save()
        return HttpResponseRedirect(request.GET.get('next', reverse('homepage')))
    data = {
        "title": this_recipe.title,
        "description": this_recipe.time_required,
        "time_required": this_recipe.description,
        "instruction": this_recipe.instruction,
        "author": this_recipe.author,
    }
    form = EditRecipeForm(initial=data)
    return render(request, "generic_form.html", {'form': form})


def author_favorite(request, author_id):
    authors_recipes = Recipe.objects.filter(author=Author.objects.get(id=author_id))
    this_author = Author.objects.filter(id=author_id).first()
    return render(request, 'generic_form.html', {'author': this_author, "recipes": authors_recipes})


@login_required
def favorite_recipe(request, recipe_id):
    if Favorites.objects.filter(author=Author.objects.get(user=request.user), recipe=Recipe.objects.get(id=recipe_id)):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('homepage')))
    else:
        Favorites.objects.create(
            author=Author.objects.get(user=request.user),
            recipe=Recipe.objects.get(id=recipe_id),
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('homepage')))