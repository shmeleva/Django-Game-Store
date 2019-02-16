import uuid

from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate

from decimal import Decimal
from enum import Enum

from game_store.apps.users.models import UserProfile
from game_store.apps.games.models import Game

class TransactionStatus(Enum):
    Pending = 'P'
    Succeeded = 'S'
    Failed = 'F'
    Canceled = 'C'

class PurchaseQuerySet(models.QuerySet):
    # Get all player successful (paid) purchases:
    def get_paid_purchases(self, player):
        return self.values('game').filter(user__exact=player, status=TransactionStatus.Succeeded.value)

    # Get a successful (paid) purchase for the specific game or None:
    def get_paid_purchase(self, player, game):
        return self.filter(user=player, game=game, status=TransactionStatus.Succeeded.value).first()

    def get_sales(self, developer):
        return self.filter(game__developer=developer).order_by('-timestamp')

    def get_sales_per_game(self, developer):
        return self.filter(game__developer=developer, status=TransactionStatus.Succeeded.value) \
            .values('game__id', 'game__title') \
            .annotate(total_sales=Count('game'), total_revenue=Sum('price')) \
            .order_by('-total_sales')

    def get_revenue_per_date(self, developer):
        today = timezone.now()
        start_date = today - timedelta(days=365)
        return self.filter(
            game__developer=developer,
            status=TransactionStatus.Succeeded.value,
            timestamp__range=[start_date, today],
        ) \
            .annotate(date=TruncDate('timestamp')) \
            .values('date') \
            .annotate(revenue=Sum('price')) \
            .order_by('date')

class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=1,
        choices=[(status.value, status.name) for status in TransactionStatus],
        default=TransactionStatus.Pending.value,
    )

    objects = PurchaseQuerySet.as_manager()

    def __str__(self):
        return self.user.user.username + " - " + self.game.title
