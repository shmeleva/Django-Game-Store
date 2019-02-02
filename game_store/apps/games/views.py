from django.shortcuts import render, get_object_or_404
from .models import Game
from game_store.apps.purchases.models import Purchase
from game_store.apps.users.models import UserProfile

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
    return render(req, 'publish.html')
