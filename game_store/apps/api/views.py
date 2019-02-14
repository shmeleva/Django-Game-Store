from django.shortcuts import render
from django.db.models import Q
from functools import reduce

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from game_store.apps.games.models import Game
from game_store.apps.categories.models import Category
from game_store.apps.results.models import Result

from .serializers import GamesSerializer, ResultsSerializer


class ListGamesView(generics.ListAPIView):
    serializer_class = GamesSerializer

    def get_queryset(self):
        queryset = Game.objects.all()

        search_query_param = self.request.query_params.get('search', None)
        if search_query_param:
            queryset = queryset.filter(title__contains=search_query_param)

        categories_query_param = self.request.query_params.get('categories', None)
        if categories_query_param:
            categories_as_strings = categories_query_param.split(",")
            q_list = map(lambda n: Q(title__iexact=n), categories_as_strings)
            q_list = reduce(lambda a, b: a | b, q_list)
            categories =  Category.objects.filter(q_list)
            if categories.exists():
                queryset = queryset.filter(categories__in=categories).distinct()
            else:
                queryset = Game.objects.none()

        return queryset


class RetrieveGameView(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = GamesSerializer
    queryset = Game.objects.all()


class ListResultsView(generics.ListAPIView):
    serializer_class = ResultsSerializer

    def get_queryset(self):
        game_id = self.kwargs['id']
        queryset = Result.objects.filter(game__id__exact=game_id).order_by("-score")
        return queryset
