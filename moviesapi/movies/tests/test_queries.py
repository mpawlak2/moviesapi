from movies.queries import filter_all_movies, filter_movie_by_title
from movies.tests.base import MovieTestCase


class TestQueries(MovieTestCase):
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

        self.create_movie()
        r = filter_all_movies()
        self.assertEqual(len(r), 1)
