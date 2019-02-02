from django.shortcuts import render, get_object_or_404
from .models import Game
from game_store.apps.purchases.models import Purchase
from game_store.apps.users.models import UserProfile
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
    #TODO: Check is_authenticated and is_developer

    if req.method == 'POST':
        form = PublishForm(req, req.POST)

#        if form.is_valid():
#            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
#
#            if user is not None:
#                auth_login(req, user)
#                return redirect('/')
    else:
        form = PublishForm()

    return render(req, 'publish.html', {
        'form': form,
    })
