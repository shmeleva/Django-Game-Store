from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from game_store.apps.games.models import Game

from .serializers import GamesSerializer

class ListGamesView(generics.ListAPIView):
    serializer_class = GamesSerializer

    def get_queryset(self):
        queryset = Game.objects.all()

        query = self.request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(title__contains=query)

        category_names = self.request.query_params.get('categories', None)
        print(category_names)
        #if category_names is not None:


        return queryset

#class HelloView(APIView):
#    def get(self, request):
#        content = {'message': 'Hello, World!'}
#        return Response(content)
