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
        self.assertEqual(resp.status_code, 201, resp.json())

    def test_all_the_attributes_are_returned(self):
        """ Test attributes that should be returned in the endpoint's json."""
        data = {
            "title": "Breaking Bad",
        }
        resp = self.client.post(reverse("movies:movies"), data=data)
        self.assertEqual(resp.status_code, 201, resp.json())

        fields = (
            "id", "title", "year", 
            "rated", "released", "runtime", "genre", "director",
            "writer", "actors", "plot", "language", "country", "awards",
            "poster", "ratings", "metascore", "imdbrating", "imdbvotes",
            "imdbid", "type", "totalseasons",
        )
        resp_data = resp.json()
        for f in fields:
            self.assertIn(f, resp_data)
            self.assertNotEqual("", resp_data[f])
        self.assertEqual(data["title"], resp_data.get("title"))

    def test_should_fetch_from_db_after_created(self):
        """After the initial POST /movies/ with the specific title, every following request should
        get its movie data from the app db.
        """
        data = {
            "title": "Breaking Bad",
        }
        resp = self.client.post(reverse("movies:movies"), data=data)
        self.assertEqual(resp.status_code, 201, resp.json())
        last_id = resp.json()["id"]

        resp = self.client.post(reverse("movies:movies"), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(last_id, resp.json()["id"])

        # When passed random string, a movie title that does not exists
        data = {
            "title": "Randomsfewfohqwefnwefop",
        }
        resp = self.client.post(reverse("movies:movies"), data=data)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.json())
