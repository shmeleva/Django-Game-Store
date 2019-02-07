from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import JsonResponse
from django.db.models import Max

import logging
logger = logging.getLogger(__name__)

from .models import Game
from game_store.apps.purchases.models import Purchase
from game_store.apps.users.models import UserProfile
from game_store.apps.users.models import UserRole
from game_store.apps.categories.models import Category
from game_store.apps.results.models import Result
from game_store.apps.games.forms import PublishForm
from game_store.apps.games.forms import SearchForm
from game_store.apps.games.utils import SearchBuilder


# All games:
def games(req):

    user = UserProfile.get_user_profile_or_none(req.user)
    games = None

    if user is None:
        games = Game.objects.all()
    else:
        if user.is_player:
            games = SearchBuilder(Game.objects.all(), user).set_ownership_flags().set_highscores().games
        else:
            games = Game.objects.filter(developer__exact=user)

    return render(req, 'games.html', {
        'games': games,
        'user_profile': user,
        'search_form': SearchForm(),
    })

# Game search results:
def search(req):

    form = SearchForm(req.POST)

    if form.is_valid():

        user = UserProfile.get_user_profile_or_none(req.user)
        query = form.cleaned_data.get('query')
        categories = form.cleaned_data.get('categories')
        player_games_only = form.cleaned_data.get('player_games_only')

        if user is not None:

            if user.is_player:
                if player_games_only:
                    purchases = Purchase.objects.values('game').filter(user__exact=user)
                    return SearchBuilder(Game.objects.filter(id__in=purchases), user) \
                    .apply_rules(query,categories) \
                    .set_ownership_flags(False) \
                    .set_highscores() \
                    .build()
                else:
                    return SearchBuilder(Game.objects, user) \
                    .apply_rules(query, categories) \
                    .set_ownership_flags() \
                    .set_highscores() \
                    .build()

            if user.is_developer:
                return SearchBuilder(Game.objects.filter(developer__exact=user), user) \
                .apply_rules(query,categories) \
                .build()

        return SearchBuilder(Game.objects, user) \
        .apply_rules(query, categories) \
        .build()
    else:
        return JsonResponse({ }) #TODO

# A game:
def game(req, id):

    user = UserProfile.get_user_profile_or_none(req.user)
    game = get_object_or_404(Game, pk=id)

    highscores = Result.objects.values('user').annotate(highscore=Max('score')).order_by('-highscore')[:10]
    logger.error(highscores)

    if Purchase.objects.filter(user=user, game=game).count() > 0:
        result = Result.objects.filter(user=user, game=game).aggregate(Max('score'))
        highscore = result['score__max'] if result is not None else 0
    return render(req, 'game.html', {
        'game': game,
        'user_profile': user,
        'score': 0,

    })

def play(req, id):
    return render(req, 'play.html', { 'game': get_object_or_404(Game, pk=id) })

def publish(req):

    user = UserProfile.get_user_profile_or_none(req.user)
    if user is None or not user_profile.is_developer:
        return redirect('/')

    if req.method == 'POST':
        form = PublishForm(req.POST, req.FILES)
        form.instance.developer = user
        if form.is_valid():
            game = form.save()
            return redirect('/game/' + str(game.id))

    else:
        form = PublishForm()

    return render(req, 'publish.html', {
        'form': form,
        'user_profile': user,
    })
