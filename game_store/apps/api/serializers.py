from rest_framework import serializers

from game_store.apps.games.models import Game
from game_store.apps.categories.models import Category
from game_store.apps.results.models import Result
from game_store.apps.users.models import UserProfile


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title")

class GamesSerializer(serializers.ModelSerializer):
    categories = CategoriesSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ("id", "title", "image", "description", "price", "categories")

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "username"]

class ResultsSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)

    class Meta:
        model = Result
        fields = ("id", "user", "score", "timestamp")
