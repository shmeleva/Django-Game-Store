from django import template
from game_store.apps.games.models import Game
from game_store.apps.purchases.models import Purchase
from game_store.apps.results.models import Result

register = template.Library()

@register.inclusion_tag("game__button.html")
def get_button(user, game):
    return {
        'user_profile': user,
        'game': game,
        'is_paid': Purchase.objects.get_paid_purchase(user, game) is not None,
        'high_score': Result.objects.get_high_score_as_int(user, game)
    }
