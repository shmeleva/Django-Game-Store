from rest_framework import serializers

from game_store.apps.games.models import Game
from game_store.apps.categories.models import Category


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title")

class GamesSerializer(serializers.ModelSerializer):
    categories = CategoriesSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ("id", "title", "image", "description", "price", "categories")
