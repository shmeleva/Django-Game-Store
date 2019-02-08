from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

import logging
logger = logging.getLogger(__name__)

from .models import Game
from game_store.apps.purchases.models import Purchase
from game_store.apps.users.models import UserProfile
from game_store.apps.users.models import UserRole
from game_store.apps.categories.models import Category
from game_store.apps.results.models import Result
from game_store.apps.games.forms import SearchForm, PublishForm, EditForm
from game_store.apps.games.utils import SearchBuilder


# All games.
# Accepts: GET / requests.
# Returns: an HttpResponse containing a rendered HTML page.
def games(req):

    if req.method != 'GET':
        return HttpResponseNotFound()

    user = UserProfile.get_user_profile_or_none(req.user)
    games = None

    if user:
        if user.is_player:
            # Setting ownership and highscore fields for player-owned games.
            games = SearchBuilder(Game.objects.all(), user) \
            .set_ownership_flags() \
            .set_highscores().games
        if user.is_developer:
            # Only showing developers their own games.
            games = Game.objects.filter(developer__exact=user)

    # Showing all games for all other users:
    if games is None:
        games = Game.objects.all()

    return render(req, 'games.html', {
        'games': games,
        'user_profile': user,
        'search_form': SearchForm(),
    })

# Search results.
# Accepts: POST /search requests.
# Returns: a JsonResponse containing a rendered HTML partial view.
def search(req):

    if req.method != 'POST':
        return HttpResponseNotFound()

    form = SearchForm(req.POST)

    if form.is_valid():
        user = UserProfile.get_user_profile_or_none(req.user)
        query = form.cleaned_data.get('query')
        categories = form.cleaned_data.get('categories')
        player_games_only = form.cleaned_data.get('player_games_only')

        if user:

            if user.is_player:
                if player_games_only:
                    # Only showing player-owned games.
                    purchases = Purchase.objects.values('game').filter(user__exact=user)
                    return SearchBuilder(Game.objects.filter(id__in=purchases), user) \
                    .apply_rules(query,categories) \
                    .set_ownership_flags(False) \
                    .set_highscores() \
                    .build()
                else:
                    # Searching through all games, while setting correct ownership
                    # and highscore fields for player-owned games.
                    return SearchBuilder(Game.objects, user) \
                    .apply_rules(query, categories) \
                    .set_ownership_flags() \
                    .set_highscores() \
                    .build()

            if user.is_developer:
                # Only searching through games publised by the developer.
                return SearchBuilder(Game.objects.filter(developer__exact=user), user) \
                .apply_rules(query,categories) \
                .build()

        # For all other users, including unauthorized users,
        # searching through all games.
        return SearchBuilder(Game.objects, user) \
        .apply_rules(query, categories) \
        .build()
    else:
        return JsonResponse({ }) #TODO

# A game.
# Accepts: GET /game/{id} requests.
# Returns: an HttpResponse containing a rendered HTML page.
# Errors:
# - 403, if game does exist but the user has no access to see the game
# (e.g. developers can only see and manage their own games).
# - 404, if Game.DoesNotExist.
def game(req, id):

    if req.method != 'GET':
        return HttpResponseNotFound()

    user = UserProfile.get_user_profile_or_none(req.user)
    game = get_object_or_404(Game, pk=id)

    if user and user.is_developer and game.developer.id != user.id:
        return HttpResponseForbidden()

    # Getting global highscores:
    global_highscores = Result.objects.filter(game=game) \
    .values('user__user__username') \
    .annotate(highscore=Max('score')) \
    .order_by('-highscore')[:10]

    context = {
        'game': game,
        'user_profile': user,
        'global_highscores': global_highscores
    }

    # Getting a personal highscore and last score for players, if available:
    if user and user.is_player:
        results = Result.objects.filter(user=user, game=game)
        if results.exists():
            context['player_highscore'] = results.order_by('-score').first()
            context['player_last_score'] = results.order_by('-timestamp').first()

    return render(req, 'game.html', context)

def play(req, id):
    return render(req, 'play.html', { 'game': get_object_or_404(Game, pk=id) })

# A game publication form.
# Accepts: GET /publish and POST /publish requests.
# Returns: HttpResponse with an HTML page for GET requests,
# a redirect to /game/{id} for successful POST requests
# Errors:
# - Redirects non-developers to /. TODO: return 401 instead
@login_required(login_url='/login/')
def publish(req):
    user = UserProfile.get_user_profile_or_none(req.user)

    # Only developers can publish games:
    if user is None or not user_profile.is_developer:
        return HttpResponseForbidden()

    if req.method == 'GET':
        return render(req, 'publish.html', {
            'form': PublishForm(),
            'user_profile': user,
        })

    if req.method == 'POST':
        form = PublishForm(req.POST, req.FILES)
        form.instance.developer = user
        if form.is_valid():
            game = form.save()
            return redirect('/game/' + str(game.id))

    return HttpResponseNotFound()


# A game editing form.
# Accepts: GET /game/{id}/edit and POST /game/{id}/edit requests.
# Returns: HttpResponse with an HTML page for GET requests,
# a redirect to /game/{id} for successful POST requests
# Errors:
# - Redirects non-developers to /. TODO: return 401 instead
# - 401, if the developer does not own the game.
@login_required(login_url='/login/')
def edit(req, id):

    logger.error(req.method)

    user = UserProfile.get_user_profile_or_none(req.user)
    game = get_object_or_404(Game, pk=id)

    if user is None or game.developer.id != user.id:
        return HttpResponseForbidden()

    if req.method == 'GET':
        initial = {}
        return render(req, 'edit.html', {
            'user_profile': user,
            'game': game,
            'form': EditForm(initial=model_to_dict(game))
        })
    elif req.method == 'POST':
        form = EditForm(req.POST, req.FILES, instance=game)
        if form.is_valid():
            form.save()

#            game.description = form.cleaned_data.get('description')
#            game.price = form.cleaned_data.get('price')
#            game.url = form.cleaned_data.get('url')
#            game.categories.set(form.cleaned_data.get('categories'))
#
#            image = form.cleaned_data.get('image')
#
#            if image:
#                game.image = image
#
#            game.save()
#
            return redirect('/game/' + str(game.id))
        else:
            return render(req, 'edit.html', {
                'user_profile': user,
                'game': game,
                'form': form
            })
    else:
        return HttpResponseNotFound()
