from django.db.models import Max
from django.template.loader import render_to_string
from django.http import JsonResponse

from game_store.apps.purchases.models import Purchase
from game_store.apps.users.models import UserProfile
from game_store.apps.users.models import UserRole
from game_store.apps.categories.models import Category
from game_store.apps.results.models import Result

class SearchBuilder:
    def __init__(self, games, user):
        self.games = games
        self.user = user

    # For all users:
    def apply_rules(self, query, categories):
        self.games = self.games.filter(title__contains=query)
        if categories.count() != 0:
            self.games = self.games.filter(categories__in=categories).distinct()
        return self

    # For players only:
    def set_ownership_flags(self, validate_ownership=True):
        if not self.user.is_player:
            raise ValueError('Ownership can only be set for players.')
        for game in self.games:
            game.is_owned = Purchase.objects.filter(user=self.user, game=game).count() > 0 if validate_ownership else True
        return self

    # For players only:
    def set_highscores(self):
        if not self.user.is_player:
            raise ValueError('Highscores can only be set for players.')
        for game in self.games:
            result = Result.objects.filter(user=self.user, game=game).aggregate(Max('score'))
            game.highscore = result['score__max'] if result is not None else 0
        return self

    def build(self):
        rendered = render_to_string('game_search_results.html', {
            'user_profile': self.user,
            'games': self.games,
        })
        return JsonResponse({ 'rendered': rendered })
