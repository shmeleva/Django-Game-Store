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
from game_store.apps.games.forms import SearchForm, PublishForm, EditForm, DeleteForm
from game_store.apps.games.utils import SearchBuilder


# All games.
# Accepts: GET requests.
# Returns: an HttpResponse containing a rendered HTML page.
def games(req):
    #
    user = UserProfile.get_user_profile_or_none(req.user)
    #
    if req.method == 'GET':
        if user:
            if user.is_player:
                # Setting ownership and highscore fields for player-owned games.
                games = SearchBuilder(Game.objects.all(), user) \
                .set_ownership_flags() \
                .set_highscores().games
            elif user.is_developer:
                # Only showing developers their own games.
                games = Game.objects.filter(developer__exact=user)
            else:
                games = Game.objects.all()
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
    #
    if user and user.is_developer:
        # Only searching through games publised by the developer.
        return SearchBuilder(Game.objects.filter(developer__exact=user), user) \
        .apply_rules(query,categories) \
        .build()
    #
    # For all other users, including unauthorized users,
    # searching through all games.
    return SearchBuilder(Game.objects, user) \
    .apply_rules(query, categories) \
    .build()

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
    # Getting global highscores:
    global_highscores = Result.objects.filter(game=game) \
    .values('user__user__username') \
    .annotate(highscore=Max('score')) \
    .order_by('-highscore')[:10]
    #
    context = {
        'game': game,
        'user_profile': user,
        'global_highscores': global_highscores,
        #
        'og_title': game.title,
        'og_description': game.description,
        'og_image': game.image.url,
    }
    #
    # Getting a personal highscore and last score for players, if available:
    if user and user.is_player:
        #
        purchase = Purchase.objects.filter(user=user, game=game)
        if purchase.exists():
            context["is_owned"] = True
            #
            results = Result.objects.filter(user=user, game=game)
            if results.exists():
                context['player_highscore'] = results.order_by('-score').first()
                context['player_last_score'] = results.order_by('-timestamp').first()
    #
    return render(req, 'game.html', context)

def play(req, id):
    return render(req, 'play.html', { 'game': get_object_or_404(Game, pk=id) })

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
