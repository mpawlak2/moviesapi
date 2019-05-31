import datetime

from django.test import TestCase

from movies.models import Movie
from movies.queries import filter_movie_by_title


class TestQueries(TestCase):
    def test_filter_movie_by_title(self):
        r = filter_movie_by_title(None)
        self.assertEqual(len(r), 0)

        # Movie does not exist.
        r = filter_movie_by_title("Breaking bad")
        self.assertEqual(len(r), 0)

        # After creating a movie
        m = Movie.objects.create(
            title="Breaking bad",
            released=datetime.date.today(),
            runtime=90,
            imdbrating=9,
        )
        r = filter_movie_by_title("Breaking bad")
        self.assertEqual(len(r), 1)
        self.assertIn(m, r)

        # Case insensitive
        r = filter_movie_by_title("breaKing BaD")
        self.assertEqual(len(r), 1)
        self.assertIn(m, r)
