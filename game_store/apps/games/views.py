from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponse
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
import json

import logging
logger = logging.getLogger(__name__)

from .models import Game, GameState
from game_store.apps.purchases.models import Purchase
from game_store.apps.users.models import UserProfile
from game_store.apps.users.models import UserRole
from game_store.apps.categories.models import Category
from game_store.apps.results.models import Result
from game_store.apps.games.forms import SearchForm, PublishForm, EditForm, DeleteForm


# All games.
# Accepts: GET requests.
# Returns: an HttpResponse containing a rendered HTML page.
def games(req):
    #
    user = UserProfile.get_user_profile_or_none(req.user)
    #
    if req.method == 'GET':
        if user and user.is_developer:
            games = Game.objects.get_published_games(user)
        else:
            games = Game.objects.all()
        #
        return render(req, 'games.html', {
            'games': games,
            'user_profile': user,
            'search_form': SearchForm(),
        })
    else:
        return HttpResponseNotFound()

# Search results.
# Accepts: POST requests.
# Returns: a JsonResponse containing a rendered HTML partial view.
# Errors:
# - 400
def search(req):
    #
    form = SearchForm(req.POST)
    #
    if not form.is_valid():
        return JsonResponse({ }, status=400)
    #
    user = UserProfile.get_user_profile_or_none(req.user)
    query = form.cleaned_data.get('query')
    categories = form.cleaned_data.get('categories')
    #
    if user and user.is_player:
        if form.cleaned_data.get('player_games_only'):
            # Only showing player-owned games:
            games = Game.objects.get_paid_games(user).search(query, categories)
        else:
            # Searching through all games:
            games = Game.objects.search(query, categories)
    elif user and user.is_developer:
        # Only searching through games publised by the developer.
        games = Game.objects.get_published_games(user).search(query, categories)
    else:
        # For all other users, including unauthorized users,
        # searching through all games.
        games = Game.objects.search(query, categories)
    #
    rendered = render_to_string('games__search-results.html', {
        'user_profile': user,
        'games': games,
    })
    return JsonResponse({ 'rendered': rendered })

# A game.
# Accepts: GET requests.
# Returns: an HttpResponse containing a rendered HTML page.
# Errors:
# - 403, if the game does exist but the user has no access
# (e.g. developers can only see and manage their own games).
# - 404, if the game does not exist.
def game(req, id):
    #
    if req.method != 'GET':
        return HttpResponseNotFound()
    #
    user = UserProfile.get_user_profile_or_none(req.user)
    game = get_object_or_404(Game, pk=id)
    #
    if user and user.is_developer and game.developer.id != user.id:
        return HttpResponseForbidden()
    #
    context = {
        'game': game,
        'user_profile': user,
        'og_title': game.title,
        'og_description': game.description,
        'og_image': game.image.url,
    }
    #
    # Getting global high scores:
    context["global_high_scores"] = Result.objects.get_global_high_scores(game)
    #
    # Getting a personal highscore and last score for players, if available:
    if user and user.is_player:
        purchase = Purchase.objects.get_paid_purchase(user, game)
        if purchase:
            context["is_paid"] = True
            if Result.objects.get_scores(user, game).exists():
                context['player_high_score'] = Result.objects.get_high_score_as_int(user, game)
                context['player_latest_score'] = Result.objects.get_latest_score_as_int(user, game)
    #
    return render(req, 'game.html', context)

def play(req, id):
    return render(req, 'play.html', { 'game': get_object_or_404(Game, pk=id) })

def update_score(req):
    user = UserProfile.get_user_profile_or_none(req.user)
    game = get_object_or_404(Game, pk=req.POST['id'])
    if user and user.is_player:
        Result(user=user, game=game, score=req.POST['score']).save()
    return HttpResponse()

def save_game(req):
    user = UserProfile.get_user_profile_or_none(req.user)
    game = get_object_or_404(Game, pk=req.POST['id'])
    if user and user.is_player:
        if GameState.objects.filter(user=user, game=game):
            GameState.objects.get(user=user, game=game).delete()
        game_state = GameState(user=user, game=game, game_state=req.POST['game_state'])
        game_state.save()
    return HttpResponse()

def load_game(req):
    user = UserProfile.get_user_profile_or_none(req.user)
    game = get_object_or_404(Game, pk=req.POST['id'])
    data = {}
    data['head'] = 'ERROR'
    data['body'] = 'Previous save not found'
    if user and user.is_player:
        if GameState.objects.filter(user=user, game=game):
            data['head'] = 'LOAD'
            data['body'] = GameState.objects.get(user=user, game=game).game_state
    return HttpResponse(json.dumps(data))

# A game publication form.
# Accepts: GET and POST requests.
# Returns: an HttpResponse with a rendered HTML page for GET requests,
# a redirect to /game/<id> for successful POST requests.
# Errors:
# - 403, if the user is not a developer
@login_required(login_url='/login/')
def publish(req):
    user = UserProfile.get_user_profile_or_none(req.user)
    #
    # Validating that the user is a developer:
    if user is None or not user.is_developer:
        return HttpResponseForbidden()
    #
    if req.method == 'GET':
        return render(req, 'publish.html', {
            'form': PublishForm(),
            'user_profile': user,
        })
    elif req.method == 'POST':
        form = PublishForm(req.POST, req.FILES)
        form.instance.developer = user
        if form.is_valid():
            game = form.save()
            return redirect("/game/{}".format(game.id))
        else:
            return render(req, 'publish.html', {
                'user_profile': user,
                'form': form
            })
    else:
        return HttpResponseNotFound()


# A game editing form.
# Accepts: GET and POST requests.
# Returns: an HttpResponse with a rendered HTML page for GET requests,
# a redirect to /game/<id> for successful POST requests.
# Errors:
# - 403, if the user is not a developer of the developer does not own the game.
# - 404, if the game does not exist.
@login_required(login_url='/login/')
def edit(req, id):
    user = UserProfile.get_user_profile_or_none(req.user)
    game = get_object_or_404(Game, pk=id)
    #
    # Validating that the user is the one who published the game:
    if user is None or game.developer.id != user.id:
        return HttpResponseForbidden()
    #
    # Returning a pre-populated edit form:
    if req.method == 'GET':
        return render(req, 'edit.html', {
            'user_profile': user,
            'game': game,
            'form': EditForm(initial=model_to_dict(game))
        })
    # Validating and saving changes to the game:
    elif req.method == 'POST':
        form = EditForm(req.POST, req.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect("/game/{}".format(game.id))
        else:
            return render(req, 'edit.html', {
                'user_profile': user,
                'game': game,
                'form': form
            })
    else:
        return HttpResponseNotFound()


# A game removal form.
# Accepts: GET and POST requests.
# Returns: an HttpResponse with a rendered HTML page for GET requests,
# a redirect to / for successful POST requests.
# Errors:
# - 403, if the user is not a developer of the developer does not own the game.
# - 404, if the game does not exist.
@login_required(login_url='/login/')
def delete(req, id):
    user = UserProfile.get_user_profile_or_none(req.user)
    game = get_object_or_404(Game, pk=id)
    #
    # Validating that the user is the one who published the game:
    if user is None or game.developer.id != user.id:
        return HttpResponseForbidden()
    #
    # Returning a removal form:
    if req.method == 'GET':
        return render(req, 'delete.html', {
            'user_profile': user,
            'game': game,
            'form': DeleteForm()
        })
    # Validating and deleting the game:
    elif req.method == 'POST':
        form = DeleteForm(req.POST)
        if form.is_valid():
            game.delete()
            return redirect("/")
        else:
            return render(req, 'delete.html', {
                'user_profile': user,
                'game': game,
                'form': form
            })
    else:
        return HttpResponseNotFound()
