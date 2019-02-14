from django.urls import path
from .views import ListGamesView

app_name = 'api'

urlpatterns = [
    # Public URLs:
    #path('games', ListGamesView.as_view(), name="games"),
    #path('games/<int:id>', ListGamesView.as_view(), name="game"),

    # Developer URLs:
    #path('developer/games', ListGamesView.as_view(), name="developer-games"),
    #path('developer/stats/', ListGamesView.as_view(), name="developer-games")
]
