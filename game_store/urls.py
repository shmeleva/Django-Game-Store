"""game_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from game_store import views
from game_store.apps.users import views as users_views
from game_store.apps.games import views as games_views
from game_store.apps.purchases import views as purchases_views

urlpatterns = [
    path('', games_views.games), # Unauthorized users can and players
    # can search games, players can also see their games, developers
    # can only search their own games and add new games.
    path('login/', users_views.login, name='login'), # Only for unauthorized users.
    path('logout/', users_views.logout, name='logout'),
    path('register/', users_views.register, name='register'),
    path('game/<int:id>', games_views.game), # Unauthorized users can sign in,
    # players can buy and play a game, developers can edit a game
    path('game/<int:id>/purchase', purchases_views.purchase), # Only for players.
    path('game/<int:id>/play', games_views.play), # Only for players.
    path('publish', games_views.publish), # Only for developers.
    path('stats', purchases_views.stats), # Only for developers.
]
