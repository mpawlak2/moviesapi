import requests
from moviesapi import settings
from rest_framework.serializers import ValidationError


def get_omdbapi_movie_by_title(title: str, raise_exception=True):
    """Query the OMDB API with use of the requests lib.

    Arguments:

        title is a movie title that you want to find
    """
    r = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={settings.OMDB_API_KEY}")
    if r.status_code != 200:
        raise ValidationError({"error": "Could not establish connection to the external API."})
    elif "Error" in r.json():
        raise ValidationError({"error": r.json()["Error"]})

    return r.json()
