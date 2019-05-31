from django.test import TestCase
from django.shortcuts import reverse


class TestMovieModel(TestCase):
    def test_get_movies_endpoint(self):
        resp = self.client.get(reverse("movies:movies"))
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.json())

    def test_should_fetch_movie_from_external_api(self):
        """The POST /movies endpoint should fetch movie data and add it to the database"""

        # When passed without a title should return status code 400.
        resp = self.client.post(reverse("movies:movies"))
        self.assertEqual(resp.status_code, 400)
        self.assertIn("title", resp.json())

        data = {
            "title": "Breaking Bad",
        }
        resp = self.client.post(reverse("movies:movies"), data=data)
        self.assertEqual(resp.status_code, 201)
        self.assertIn("title", resp.json())
        self.assertEqual(data["title"], resp.json().get("title"))

        # When passed random string, a movie title that does not exists
        data = {
            "title": "Randomsfewfohqwefnwefop",
        }
        resp = self.client.post(reverse("movies:movies"), data=data)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.json())
