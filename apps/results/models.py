from django.db import models
from apps.users.models import UserProfile
from apps.games.models import Game

class Result(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
