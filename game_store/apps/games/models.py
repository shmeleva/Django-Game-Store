from django.db import models
from django.core.validators import MinValueValidator
from game_store.apps.users.models import UserProfile
from game_store.apps.categories.models import Category
from decimal import *

class Game(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    url = models.URLField(max_length=128)
    developer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True) # TODO: Make blank=False

    def __str__(self):
        return self.title
