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
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from game_store import views
from game_store.apps.users import views as users_views
from game_store.apps.games import views as games_views
from game_store.apps.results import views as results_views
from game_store.apps.purchases import views as purchases_views
from game_store.apps.api import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', games_views.games, name='default_view'), # Unauthorized users and players
    # can search games, players can also see their games, developers
    # can only search their own games and add new games.
    path('search', games_views.search, name = 'search'),
    path('login/', users_views.login, name='login'), # Only for unauthorized users.
    path('logout/', users_views.logout, name='logout'),
    path('register/', users_views.register, name='register'),
    path('verify/<encoded_uid>/<token>/', users_views.verify),
    path('profile/edit/', users_views.edit_profile, name='edit_profile'),
    path('profile/password/', users_views.change_password),
    path('game/<int:id>', games_views.game, name='game_page'), # Unauthorized users can sign in,
    # players can buy and play a game, developers can edit a game
    path('game/<int:id>/edit', games_views.edit, name='edit'), # Only for developers.
    path('game/<int:id>/delete', games_views.delete, name='delete'), # Only for developers.
    path('game/<int:id>/purchase', purchases_views.purchase, name='purchase'), # Only for players.
    path('game/<int:id>/play', games_views.play, name='play'), # Only for players.
    path('game/update_score', games_views.update_score, name='update_score'),
    path('game/save_game', games_views.save_game, name='save_game'),
    path('game/load_game', games_views.load_game, name='load_game'),
    path('publish', games_views.publish, name='publish'), # Only for developers.
    path('stats', purchases_views.stats, name='stats'), # Only for developers.
    path('payment/result', purchases_views.payment_result),
    path('test/test', purchases_views.payment_result),
    path('api/games/', api_views.ListGamesView.as_view()),
    #path('api/games/', include('games.urls')),
    #re_path('api/(?P<version>(v1|v2))/', include('api.urls', namespace='game_store')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
