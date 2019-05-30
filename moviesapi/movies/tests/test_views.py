from django.test import TestCase
from django.shortcuts import reverse


class TestMovieModel(TestCase):
    def test_get_movies_endpoint(self):
        resp = self.client.get(reverse("movies:movies"))
        self.assertEqual(resp.status_code, 200)
