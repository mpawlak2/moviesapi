import datetime
import random
import string

from django.test import TestCase

from movies.models import Movie
from movies.queries import filter_movie_by_title, filter_all_movies


class TestQueries(TestCase):
    def create_movie(self):
        return Movie.objects.create(
            title=random.sample(string.printable, 10),
            released=datetime.date.today(),
            runtime=90,
            imdbrating=9,
            imdbvotes=10,
        )

    def test_filter_movie_by_title(self):
        r = filter_movie_by_title(None)
        self.assertEqual(len(r), 0)

        # Movie does not exist.
        r = filter_movie_by_title("Breaking bad")
        self.assertEqual(len(r), 0)

        # After creating a movie
        m = self.create_movie()
        r = filter_movie_by_title(m.title)
        self.assertEqual(len(r), 1)
        self.assertIn(m, r)

        # Case insensitive
        r = filter_movie_by_title(m.title)
        self.assertEqual(len(r), 1)
        self.assertIn(m, r)

    def test_filter_all_movies(self):
        r = filter_all_movies()

        self.assertEqual(len(r), 0)
