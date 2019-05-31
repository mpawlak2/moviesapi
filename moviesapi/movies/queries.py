import datetime

from django.db.models import Count, Window, F, Q
from django.db.models.functions import DenseRank

from movies.models import Movie, Comment


def filter_movie_by_title(title: str):
    """Return movie with an exact title match."""
    if title:
        return Movie.objects.filter(title__iexact=title)
    return Movie.objects.all()


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


def filter_top_movies(date_from: datetime.date, date_to: datetime.date):
    """Return all movies with total_comments and rank fields.

    total_comments is a total number of comments that were added between specified date range
    """
    comments_within_date_range = Q(comments__created_at__date__gte=date_from) & Q(comments__created_at__date__lte=date_to)
    qs = Movie.objects.annotate(
        total_comments=Count("comments", filter=comments_within_date_range),
        rank=Window(
            expression=DenseRank(),
            order_by=F("total_comments").desc(),
        )
    )
    return qs
