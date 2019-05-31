import datetime

from django.utils import timezone

from movies.queries import (filter_all_comments, filter_all_movies,
                            filter_movie_by_title, filter_top_movies)
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

    def test_filter_all_comments(self):
        """Test the filter_all_comments query."""
        r = filter_all_comments()
        self.assertEqual(len(r), 0)

        m = self.create_movie()
        c = self.create_comment(m.id, "Testing")

        r = filter_all_comments()
        self.assertEqual(len(r), 1)
        self.assertIn(c, r)

    def test_top_movies_statistics(self):
        """Query that returns all movies from the database with some annotated fields.

        Every movie should have `total_comments` field and `rank` field.
        """
        r = filter_top_movies(timezone.now().date(), timezone.now().date())
        self.assertEqual(len(r), 0)

        # There should be only one movie with 0 total_comments and 1 as rank
        m = self.create_movie()
        r = filter_top_movies(timezone.now().date(), timezone.now().date())
        self.assertEqual(len(r), 1)

        movie = r[0]
        self.assertEqual(movie.total_comments, 0)
        self.assertEqual(movie.rank, 1)

        # Add another movie without any comment.
        m = self.create_movie()
        r = filter_top_movies(timezone.now().date(), timezone.now().date()).order_by("-id")
        self.assertEqual(len(r), 2)

        movie = r[0]
        self.assertEqual(movie.id, m.id)
        self.assertEqual(movie.total_comments, 0)
        self.assertEqual(movie.rank, 1)

        # Add a movie with one comment.
        m = self.create_movie()
        c = self.create_comment(m.id, "Test")
        r = filter_top_movies(timezone.now().date(), timezone.now().date()).order_by("-id")
        self.assertEqual(len(r), 3)

        movie = r[0]
        self.assertEqual(movie.id, m.id)
        self.assertEqual(movie.total_comments, 1)
        self.assertEqual(movie.rank, 1)
        # And those without any comments should have rank equal to 2.
        for movie in r:
            if movie.id != m.id:
                self.assertEqual(movie.rank, 2)

    def test_top_movies_statistics_should_ignore_comments_based_on_date(self):
        """If the date the comment was addes is not between date range specified in query, those
        comments should not be considered.
        """
        m = self.create_movie()
        c = self.create_comment(m.id, "Testing")
        c.created_at = timezone.now() + datetime.timedelta(days=1)
        c.save()

        # Query for today's statistics
        r = filter_top_movies(timezone.now().date(), timezone.now().date())
        self.assertEqual(len(r), 1)
        movie = r[0]
        self.assertEqual(movie.total_comments, 0)
