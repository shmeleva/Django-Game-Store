from django.db import models
from django.apps import apps
from django.core.validators import MinValueValidator
from game_store.apps.users.models import UserProfile
from game_store.apps.categories.models import Category
from decimal import Decimal


class GameQuerySet(models.QuerySet):
    # Filter games by query and categories:
    def search(self, query, categories):
        result = self.filter(title__icontains=query)
        if categories.count() != 0:
            result = result.filter(categories__in=categories).distinct()
        return result

    # Filter games publised by the developer:
    def get_published_games(self, user):
        return self.filter(developer__exact=user)

    # Filter games that the user paid for:
    def get_paid_games(self, user):
        paid_purchases = apps.get_model('purchases.Purchase').objects.get_paid_purchases(user)
        return self.filter(id__in=paid_purchases)


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
