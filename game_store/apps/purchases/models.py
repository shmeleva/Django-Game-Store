from django.db import models
from django.core.validators import MinValueValidator
from decimal import *
from game_store.apps.users.models import UserProfile
from game_store.apps.games.models import Game

class Purchase(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.user.user.username + " - " + self.game.title
