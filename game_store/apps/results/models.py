from django.db import models
from game_store.apps.users.models import UserProfile
from game_store.apps.games.models import Game

class Result(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
