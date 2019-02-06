from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from game_store.apps.games.models import Game
from game_store.apps.purchases.models import Purchase
from game_store.apps.purchases.forms import PurchaseForm

@login_required(login_url='/login/')
def purchase(req, id):
    # TODO: Check if the user has already purchased the game

    game = get_object_or_404(Game, pk=id)

    if req.method == 'POST':
        form = PurchaseForm(req.POST)

        if form.is_valid():
            # TODO: Call the API
    else:
        form = PurchaseForm()

    return render(req, 'purchase.html', {
        'form': form,
        'game': game,
    })

def stats(req):
    return render(req, 'stats.html')
