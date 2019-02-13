import logging
import os
import uuid
from hashlib import md5
from collections import OrderedDict
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from game_store.apps.games.models import Game
from game_store.apps.purchases.models import Purchase, TransactionStatus
from game_store.apps.purchases.forms import PurchaseForm
from game_store.apps.users.models import UserProfile
from game_store.apps.purchases.fusioncharts import FusionCharts

logger = logging.getLogger(__name__)

@login_required(login_url='/login/')
def purchase(req, id):
    user_profile = UserProfile.get_user_profile_or_none(req.user)
    if user_profile is None or user_profile.is_developer:
        logger.error('The user is not allowed to purchase a game: {}'.format(req.user.username))
        return HttpResponseForbidden() # FIXME: Handle it the other way

    if Purchase.objects.filter(user=user_profile, game=id, status=TransactionStatus.Succeeded.value).exists():
        return redirect('/game/{}'.format(id))

    game = get_object_or_404(Game, pk=id)

    try:
        purchase = Purchase.objects.filter(user=user_profile, game=game, status=TransactionStatus.Pending.value)[0:1].get()
        purchase.price = game.price
    except Purchase.DoesNotExist:
        purchase = Purchase(user=user_profile, game=game, price=game.price)

    purchase.save()

    formatted_pid = purchase.id.hex
    sid = os.environ.get('PAYMENT_SID', '')
    secret_key = os.environ.get('PAYMENT_SECRET_KEY', '')
    redirect_url = '{}/payment/result'.format(settings.HOST)

    checksum_input = 'pid={}&sid={}&amount={}&token={}'.format(formatted_pid, sid, game.price, secret_key)
    m = md5(checksum_input.encode('ascii'))
    checksum = m.hexdigest()

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

# TODO: Render user-friendly UI and improve other error responses
def payment_result(req):
    formatted_pid = req.GET.get('pid')
    ref = req.GET.get('ref')
    result = req.GET.get('result')
    checksum = req.GET.get('checksum')
    secret_key = os.environ.get('PAYMENT_SECRET_KEY', '')

    checksum_input = 'pid={}&ref={}&result={}&token={}'.format(formatted_pid, ref, result, secret_key)
    m = md5(checksum_input.encode('ascii'))
    calculated_checksum = m.hexdigest()

    pid = uuid.UUID(formatted_pid)

    if checksum != calculated_checksum:
        logger.error('Checksum mismatch: {}'.format(pid))
        return HttpResponse(status=400)

    try:
        purchase = Purchase.objects.get(id=pid)
    except Purchase.DoesNotExist:
        return HttpResponse(status=404)
    
    if purchase.status != TransactionStatus.Pending.value:
        logger.error('Duplicated payment result: {}'.format(pid))
        return HttpResponseForbidden()

    if result == 'cancel':
        status = TransactionStatus.Canceled.value
    elif result == 'success':
        status = TransactionStatus.Succeeded.value
    else:
        status = TransactionStatus.Failed.value

    purchase.status = status
    purchase.save()

    if result == 'cancel':
        return redirect('/game/{}'.format(purchase.game.id))

    return render(req, 'result.html', {
        'succeeded': result == 'success',
        'game_id': purchase.game.id,
    })

@login_required(login_url='/login/')
def stats(req):
    user_profile = UserProfile.get_user_profile_or_none(req.user)
    if user_profile is None or not user_profile.is_developer:
        return HttpResponseForbidden()

    sales = Purchase.objects.filter(game__developer=user_profile).order_by('-timestamp')
    sales_per_game = Purchase.objects.filter(game__developer=user_profile, status=TransactionStatus.Succeeded.value) \
        .values('game__id', 'game__title') \
        .annotate(total_sales=Count('game'), total_revenue=Sum('price')) \
        .order_by('-total_sales')

    today = timezone.now()
    start_date = today - timedelta(days=365)
    revenue_per_date = Purchase.objects.filter(
        game__developer=user_profile,
        status=TransactionStatus.Succeeded.value,
        timestamp__range=[start_date, today],
    ) \
        .annotate(date=TruncDate('timestamp')) \
        .values('date') \
        .annotate(revenue=Sum('price')) \
        .order_by('date')

    dataSource = OrderedDict()
    chartConfig = OrderedDict()
    chartConfig['caption'] = 'Revenue'
    chartConfig['xAxisName'] = 'Date'
    chartConfig['yAxisName'] = 'Revenue (EUR)'
    chartConfig['decimals'] = '2'
    chartConfig['forceDecimals'] = '1'
    chartConfig['yAxisValueDecimals'] = '2'
    chartConfig['forceYAxisValueDecimals'] = '1'
    chartConfig['lineThickness'] = '2'
    chartConfig['theme'] = 'fusion'
    dataSource['chart'] = chartConfig
    dataSource['data'] = []

    for entry in revenue_per_date:
        data = {}
        data['label'] = str(entry.get('date'))
        data['value'] = float(entry.get('revenue'))
        dataSource['data'].append(data)

    chart = FusionCharts('line', 'revenue-chart', '100%', '400', 'revenue-chart-container', 'json', dataSource)

    return render(req, 'stats.html', {
        'sales': sales,
        'sales_per_game': sales_per_game,
        'chart': chart.render(),
    })
