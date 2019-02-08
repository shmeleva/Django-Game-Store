from django import forms
from django.forms import ModelForm
from django.forms import Form

from game_store.apps.games.models import Game
from game_store.apps.categories.models import Category

class PublishForm(ModelForm):
    class Meta:
        model = Game
        fields = ('title', 'image', 'description', 'price' , 'url', 'categories')
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            #'developer': forms.HiddenInput(),
        }

class EditForm(ModelForm):
    class Meta:
        model = Game
        fields = ('image', 'description', 'price' , 'url', 'categories')
        widgets = {
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'}),
        }

class SearchForm(Form):
    query = forms.CharField(
        label="",
        max_length=128,
        required=False
    )
    categories = forms.ModelMultipleChoiceField(
        label="",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=Category.objects.all()
    )
    player_games_only = forms.BooleanField(
        label="My Games",
        required=False
    )
