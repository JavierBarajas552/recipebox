from django import forms
from homepage.models import Author, Recipe


class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=80)
    time_required = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea)
    instruction = forms.CharField(widget=forms.Textarea)
    author = forms.ModelChoiceField(queryset=Author.objects.all())

class AddAuthorForm(forms.Form):
    name = forms.CharField(max_length=80)
    bio = forms.CharField(widget=forms.Textarea)