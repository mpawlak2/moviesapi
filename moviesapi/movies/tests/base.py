import datetime
import random
import string

from django.test import TestCase

from movies.models import Movie, Comment


class MovieTestCase(TestCase):
    def create_movie(self):
        return Movie.objects.create(
            title=random.sample(string.printable, 10),
            released=datetime.date.today(),
            runtime=90,
            imdbrating=9,
            imdbvotes=10,
        )

    def create_comment(self, movie_id: int, body: str) -> Comment:
        """A helper method that returns a Comment instance."""
        return Comment.objects.create(
            movie_id=movie_id,
            body=body,
        )
