from movies.models import Movie, Comment


def filter_movie_by_title(title: str):
    """Return movie with an exact title match."""
    return Movie.objects.filter(title__iexact=title)


def filter_all_movies():
    """Return all movies present in the database."""
    return Movie.objects.all()


def filter_all_comments(movie_id: int = None):
    """Return all comments present in the database, with optional filtering.

    Argumetns:
        movie_id - show only comments that are added to this movie
    """
    if movie_id:
        return Comment.objects.filter(movie_id=movie_id)
    return Comment.objects.all()
