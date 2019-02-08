import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from enum import Enum
from game_store.apps.users.models import UserProfile
from game_store.apps.games.models import Game

class TransactionStatus(Enum):
    Pending = 'P'
    Succeeded = 'S'
    Failed = 'F'

class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1,
        choices=[(status.value, status.name) for status in TransactionStatus],
        default=TransactionStatus.Pending.value,
    )

    def __str__(self):
        return self.user.user.username + " - " + self.game.title
