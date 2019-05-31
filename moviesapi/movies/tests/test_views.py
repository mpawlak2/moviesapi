import datetime

from django.shortcuts import reverse

from movies.tests.base import MovieTestCase


class TestMoviesEndpoints(MovieTestCase):
    def test_get_movies_endpoint(self):
        resp = self.client.get(reverse("movies:movies"))
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.json())

        self.create_movie()

        resp = self.client.get(reverse("movies:movies"))
        self.assertEqual(len(resp.json()), 1)

    def test_should_fetch_movie_from_external_api(self):
        """The POST /movies endpoint should fetch movie data and add it to the database"""

        # When passed without a title should return status code 400.
        resp = self.client.post(reverse("movies:movies"))
        self.assertEqual(resp.status_code, 400)
        self.assertIn("title", resp.json())
        self.assertEqual(len(resp.json()), 1)

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
            if f == "ratings":
                self.assertGreater(len(resp_data[f]), 0)
                for r in resp_data[f]:
                    self.assertIn("source", r)
                    self.assertIn("value", r)
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


class TestCommentsEndpoints(MovieTestCase):
    def test_should_get_all_comments(self):
        resp = self.client.get(reverse("movies:comments"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 0)

        m = self.create_movie()
        c = self.create_comment(m.id, "testing")
        resp = self.client.get(reverse("movies:comments"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0]["id"], c.id)

    def test_should_allow_filtering_comments_by_movie_id(self):
        m = self.create_movie()
        comments = []
        for _ in range(4):
            comments.append(self.create_comment(m.id, "Testing"))

        m2 = self.create_movie()
        for _ in range(4):
            comments.append(self.create_comment(m2.id, "Testing movie 2"))

        resp = self.client.get(reverse("movies:comments"))
        self.assertEqual(resp.status_code, 200)
        all_len = len(resp.json())
        self.assertEqual(all_len, len(comments))

        filter_kwargs = {
            "movie": m.id,
        }
        resp = self.client.get(reverse("movies:comments"), filter_kwargs)
        self.assertEqual(resp.status_code, 200)
        m_len = len(resp.json())
        self.assertLess(m_len, all_len)
        for rcomment in resp.json():
            self.assertEqual(rcomment["movie"], m.id)

        filter_kwargs = {
            "movie": m2.id,
        }
        resp = self.client.get(reverse("movies:comments"), filter_kwargs)
        self.assertEqual(resp.status_code, 200)
        m_len = len(resp.json())
        self.assertLess(m_len, all_len)
        for rcomment in resp.json():
            self.assertEqual(rcomment["movie"], m2.id)

    def test_should_create_comment(self):
        """Test that POST /comments with data consisting of movie id and body text creates a Comment in the database."""

        # body field is required
        resp = self.client.post(reverse("movies:comments"))
        self.assertEqual(resp.status_code, 400)
        self.assertIn("body", resp.json())
        self.assertIn("movie", resp.json())
        self.assertEqual(len(resp.json()), 2)

        # movie is required
        data = {
            "body": "This is a comment",
        }
        resp = self.client.post(reverse("movies:comments"), data=data)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("movie", resp.json())
        self.assertEqual(len(resp.json()), 1)

        # body and movie -> create a comment
        m = self.create_movie()
        data = {
            "body": "Testing",
            "movie": m.id,
        }
        resp = self.client.post(reverse("movies:comments"), data=data)
        self.assertEqual(resp.status_code, 201)
        self.assertIn("body", resp.json())
        self.assertIn("movie", resp.json())
        self.assertIn("id", resp.json())


class TestTopEndpoint(MovieTestCase):
    def test_should_get_top_movies_from_db(self):
        """GET /top should return all movies in the database that:

            - should annotate each entry with the number of comments
            - should require date rage as an input (e.g., date_from=...&date_to=...)
            - should count only those comments that were added between date range
            - every entry should have a rank based on the number of comments
            - entries with the same number of comments should have the same rank
        """
        resp = self.client.get(reverse("movies:top"))
        self.assertEqual(resp.status_code, 400)
        self.assertIn("date_from", resp.json())
        self.assertIn("date_to", resp.json())

        # Passed incorrect data
        data = {
            "date_from": "not a date",
            "date_to": 1234,
        }
        resp = self.client.get(reverse("movies:top"), data=data)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("date_from", resp.json())
        self.assertIn("date_to", resp.json())

        # Passed date_from that is after the date_to
        data = {
            "date_from": str(datetime.date.today() + datetime.timedelta(days=10)),
            "date_to": str(datetime.date.today()),
        }
        resp = self.client.get(reverse("movies:top"), data=data)
        self.assertEqual(resp.status_code, 400)
