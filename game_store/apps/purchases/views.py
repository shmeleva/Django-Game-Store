import logging
import os
import uuid
from hashlib import md5
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from game_store.apps.games.models import Game
from game_store.apps.purchases.models import Purchase, TransactionStatus
from game_store.apps.purchases.forms import PurchaseForm
from game_store.apps.users.models import UserProfile
from django.core.cache import cache

logger = logging.getLogger(__name__)

@login_required(login_url='/login/')
def purchase(req, id):
    user_profile = UserProfile.get_user_profile_or_none(req.user)
    if user_profile is None or user_profile.is_developer:
        logger.error('The user is not allowed to purchase a game: {}'.format(req.user.username))
        return HttpResponseForbidden() # FIXME: Handle it the other way

    if Purchase.objects.filter(user=user_profile, game=id, status=TransactionStatus.Succeeded).exists():
        return redirect('/game/{}'.format(id))

    game = get_object_or_404(Game, pk=id)

    pid = uuid.uuid4()
    formatted_pid = pid.hex
    sid = os.environ.get('PAYMENT_SID', '')
    secret_key = os.environ.get('PAYMENT_SECRET_KEY', '')
    redirect_url = '{}/payment/result'.format(settings.HOST)

    checksum_input = 'pid={}&sid={}&amount={}&token={}'.format(formatted_pid, sid, game.price, secret_key)
    m = md5(checksum_input.encode("ascii"))
    checksum = m.hexdigest()

    # A user can have one pending purchase at a time.
    prev_purchase = cache.get(user_profile.id)
    if prev_purchase is not None:
        cache.delete(prev_purchase)

    # Used for recording the payment result in payment_result
    cache.set(user_profile.id, pid)
    cache.set(pid, {
        'user_id': user_profile.id,
        'game_id': game.id,
        'price': game.price,
    })

    form = PurchaseForm()

    return render(req, 'purchase.html', {
        'form': form,
        'game': game,
        'pid': formatted_pid,
        'sid': sid,
        'amount': game.price,
        'redirect_url': redirect_url,
        'checksum': checksum,
    })

def stats(req):
    return render(req, 'stats.html')
