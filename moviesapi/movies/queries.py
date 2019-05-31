from movies.models import Movie


def filter_movie_by_title(title: str):
    return Movie.objects.filter(title__iexact=title)
