from django.shortcuts import render
from django.http import Http404
from .models import Game

def games(req):
    all_games = Game.objects.all()
    return render(req, 'games.html', { 'all_games': all_games })

def game(req, id):
    try:
        game = Game.objects.get(pk = id)
    except Game.DoesNotExist:
        raise Http404('Game does not exist')
    return render(req, 'game.html', { 'game': game })

def play(req, id):
    return render(req, 'play.html')

def publish(req):
    return render(req, 'publish.html')
