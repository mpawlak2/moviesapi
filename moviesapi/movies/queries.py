from movies.models import Movie, Comment


def filter_movie_by_title(title: str):
    """Return movie with an exact title match."""
    return Movie.objects.filter(title__iexact=title)


def filter_all_movies():
    """Return all movies present in the database."""
    return Movie.objects.all()


def filter_all_comments():
    """Return all comments present in the database."""
    return Comment.objects.all()
