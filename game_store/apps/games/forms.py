from django.forms import ModelForm
from game_store.apps.games.models import Game

class PublishForm(ModelForm):
#    role = forms.ChoiceField(
#        choices=[(role.value, role.name) for role in UserRole],
#    )

    class Meta:
        model = Game
        fields = ('title', 'image', 'description', 'price' , 'url')

    def save(self, commit=True):
        game = super(PublishForm, self).save(commit=True)
        return game
