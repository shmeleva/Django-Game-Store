def filter_games(user, query, categories, user_games_only):
    if user is not None:
        games = Game.objects.filter

    games = Game.objects.filter(title__contains=query)

    if categories.count() != 0:
        games = games.filter(categories__in=categories).distinct()

    return games
