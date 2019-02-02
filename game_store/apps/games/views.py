from django.shortcuts import render, redirect, get_object_or_404
import logging
logger = logging.getLogger(__name__)
from .models import Game
from game_store.apps.purchases.models import Purchase
from game_store.apps.users.models import UserProfile
from game_store.apps.users.models import UserRole
from game_store.apps.games.forms import PublishForm

def all_games(req):
    games = Game.objects.all()
    return render(req, 'games.html', { 'games': games })

# TODO: clean this code
def owned_games(req):
    up = get_object_or_404(UserProfile, user=req.user)
    purchases = Purchase.objects.filter(user=up)
    games = set()
    for purchase in purchases:
        games.add(purchase.game)
    return render(req, 'games.html', { 'games': games })

def game(req, id):
    game = get_object_or_404(Game, pk=id)
    return render(req, 'game.html', { 'game': game })

def play(req, id):
    return render(req, 'play.html')

def publish(req):
    # Check if the user is authenticated as a developer.
    logger.error("Publishing...")
    if not req.user.is_authenticated:
        return redirect('/')

    user_profile = get_object_or_404(UserProfile, user=req.user)
    if int(user_profile.role) != UserRole.Developer.value:
        return redirect('/')

    logger.error(req.FILES)

    if req.method == 'POST':
        form = PublishForm(req.POST, req.FILES)
        form.instance.developer = user_profile

        if form.is_valid():
            game = form.save()
            return redirect('/')
        else:
            logger.error("invalid form")

    else:
        form = PublishForm()

    return render(req, 'publish.html', {
        'form': form,
    })
