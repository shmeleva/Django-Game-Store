from django.db import models
from django.db.models import Max

from game_store.apps.users.models import UserProfile
from game_store.apps.games.models import Game


class ResultQuerySet(models.QuerySet):
    # Get player personal scores as objects:
    def get_scores(self, user, game):
        return self.filter(user=user, game=game)

    # Get player high score as an object:
    def get_high_score(self, user, game):
        return self.get_scores(user, game).order_by('-score').first()

    # Get player high score as a number:
    def get_high_score_as_int(self, user, game, default=0):
        high_score =  self.get_high_score(user, game)
        return high_score.score if high_score is not None else default

    # Get player latest score as an object:
    def get_latest_score(self, user, game):
        return self.get_scores(user, game).order_by('-timestamp').first()

    # Get player latest score as a number:
    def get_latest_score_as_int(self, user, game, default=0):
        latest_score =  self.get_latest_score(user, game)
        return latest_score.score if latest_score is not None else default

    # Get global high scores as objects:
    def get_global_high_scores(self, game, count=10):
        return self.filter(game=game) \
        .values('user__user__username') \
        .annotate(highscore=Max('score')) \
        .order_by('-highscore')[:count]


class Result(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    objects = ResultQuerySet.as_manager()

    def __str__(self):
        return self.user.user.username + " - " + self.game.title + " - " + str(self.score)
