from django.shortcuts import render, redirect, get_object_or_404
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
    games_with_scores = set()
    for game in Game.objects.all():
        g = (game, 0)
        if Result.objects.filter(user=UserProfile.get_user_profile_or_none(req.user), game=game):
            g = (game, Result.objects.get(user=UserProfile.get_user_profile_or_none(req.user), game=game).score)
        games_with_scores.add(g)
    return render(req, 'games.html', {
        'games': games_with_scores,
        'user_profile': UserProfile.get_user_profile_or_none(req.user),
        'search_form': SearchForm(),
    })

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
    return render(req, 'play.html')

def publish(req):
    user_profile = UserProfile.get_user_profile_or_none(req.user)
    if user_profile is None or not user_profile.is_developer:
        return redirect('/')

    if req.method == 'POST':
        form = PublishForm(req.POST, req.FILES)
        form.instance.developer = user_profile
        #form.instance.categories.all()

        if form.is_valid():
            game = form.save(commit=False)
            game.save()
            #form.save_m2m()
            return redirect('/game/' + str(game.id))
        else:
            logger.error("Invalid form!")

    else:
        form = PublishForm()

    return render(req, 'publish.html', {
        'form': form,
        'user_profile': user_profile,
    })
