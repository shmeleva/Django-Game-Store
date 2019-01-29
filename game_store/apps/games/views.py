from django.shortcuts import render

def games(req):
    return render(req, 'games.html')

def game(req, id):
    return render(req, 'game.html')

def play(req, id):
    return render(req, 'play.html')

def publish(req):
    return render(req, 'publish.html')
