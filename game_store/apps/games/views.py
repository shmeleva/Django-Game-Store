from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext

from django.http import JsonResponse
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

def all_games(req):
    #if req.method == 'POST':
    #else:
    games = Game.objects.all()
    for game in games:
        if Result.objects.filter(user=UserProfile.get_user_profile_or_none(req.user), game=game):
            game.score = Result.objects.get(user=UserProfile.get_user_profile_or_none(req.user), game=game).score
        else:
            game.score = 0
    return render(req, 'games.html', {
        'games': games,
        'user_profile': UserProfile.get_user_profile_or_none(req.user),
        'search_form': SearchForm(),
    })

def search(req):
    form = SearchForm(req.POST)
    if form.is_valid():
        games = Game.search(
            form.cleaned_data.get('query'),
            form.cleaned_data.get('is_purchased'),
            form.cleaned_data.get('categories'))
        rendered = render_to_string('game_search_results.html', {
            'games': games,
            'user_profile': UserProfile.get_user_profile_or_none(req.user),
        })
        return JsonResponse({'rendered': rendered})
    else:
        return JsonResponse({ })

# TODO: clean this code
def owned_games(req):
    up = get_object_or_404(UserProfile, user=req.user)
    purchases = Purchase.objects.filter(user=up)
    games = set()
    for purchase in purchases:
        games.add(purchase.game)
    return render(req, 'games.html', {
        'games': games,
        'user_profile': UserProfile.get_user_profile_or_none(req.user),
    })

def game(req, id):
    game = get_object_or_404(Game, pk=id)
    result = Result.objects.filter(user=UserProfile.get_user_profile_or_none(req.user), game=game)
    score = 0
    if result:
        score = result.first().score
    return render(req, 'game.html', {
        'game': game,
        'user_profile': UserProfile.get_user_profile_or_none(req.user),
        'score': score,
    })

def play(req, id):
    return render(req, 'play.html', { 'game': get_object_or_404(Game, pk=id) })

def publish(req):
    user_profile = UserProfile.get_user_profile_or_none(req.user)
    if user_profile is None or not user_profile.is_developer:
        return redirect('/')

    if req.method == 'POST':
        form = PublishForm(req.POST, req.FILES)
        form.instance.developer = user_profile

        if form.is_valid():
            game = form.save()
            return redirect('/game/' + str(game.id))
        else:
            logger.error("Invalid form!")

    else:
        form = PublishForm()

    return render(req, 'publish.html', {
        'form': form,
        'user_profile': user_profile,
    })
