from django.db import models
from django.apps import apps
from django.core.validators import MinValueValidator
from game_store.apps.users.models import UserProfile
from game_store.apps.categories.models import Category
from decimal import Decimal

class GameQuerySet(models.QuerySet):
    def search(self, query, categories):
        result = self.filter(title__contains=query)
        if categories.count() != 0:
            result = result.filter(categories__in=categories).distinct()
        return result

    def annotate_paid_games(self, player, validate_payment=True):
        if not player.is_player:
            raise ValueError('annotate_paid_games() can only be called for players.')
        return self.annotate(is_owned=Purchase.objects.is_paid(user, game) if validate_payment else True) \
        .annotate(is_owned=Purchase.objects.filter(user=self.user, game=game).exists() if validate_payment else True)
# .annotate(below_5=below_5).annotate(above_5=above_5)

class Game(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    url = models.URLField(max_length=128)
    developer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True) # TODO: Make blank=False

    objects = GameQuerySet.as_manager()

    def __str__(self):
        return self.title

class GameState(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    game_state = models.TextField()
