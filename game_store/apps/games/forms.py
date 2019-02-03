from django import forms
from django.forms import ModelForm
from game_store.apps.games.models import Game
from game_store.apps.categories.models import Category

class PublishForm(ModelForm):
    categories = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Category.objects.all())

    class Meta:
        model = Game
        fields = ('title', 'image', 'description', 'price' , 'url')

    def save(self, commit=True):
        game = super(PublishForm, self).save(commit=True)
        return game
