from django.shortcuts import render, redirect, get_object_or_404
import logging
logger = logging.getLogger(__name__)
from .models import Game
from game_store.apps.purchases.models import Purchase
from game_store.apps.users.models import UserProfile
from game_store.apps.users.models import UserRole
from game_store.apps.categories.models import Category
from game_store.apps.games.forms import PublishForm

def all_games(req):
    games = Game.objects.all()
    return render(req, 'games.html', {
        'games': games,
        'user_profile': UserProfile.get_user_profile_or_none(req.user),
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
    return render(req, 'game.html', {
        'game': game,
        'user_profile': UserProfile.get_user_profile_or_none(req.user),
    })

def play(req, id):
    return render(req, 'play.html')

def publish(req):
    logger.error("Publishing...")

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
            return redirect('/')
        else:
            logger.error("Invalid form!")

    else:
        form = PublishForm()

    return render(req, 'publish.html', {
        'form': form,
        'user_profile': user_profile,
    })
