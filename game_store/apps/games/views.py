from django.shortcuts import render, get_object_or_404
from .models import Game

def games(req):
    all_games = Game.objects.all()
    return render(req, 'games.html', { 'all_games': all_games })

def game(req, id):
    game = get_object_or_404(Game, pk=id)
    return render(req, 'game.html', { 'game': game })

def play(req, id):
    return render(req, 'play.html')

def publish(req):
    return render(req, 'publish.html')
