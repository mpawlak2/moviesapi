import datetime

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

    data = {key.lower(): value for key, value in r.json().items()}

    # Assuming the OMDB returns the released key value in format "20 Jan 2008"
    data["released"] = str(datetime.datetime.strptime(data["released"], r"%d %b %Y").date())

    # Assuming the OMDB returns the runtime key value in "xx min" format where xx is an integer.
    data["runtime"] = data["runtime"][:-4] if data["runtime"].endswith("min") else None
    data["ratings"] = [{key.lower(): value for key, value in r.items()} for r in data["ratings"]]
    data["imdbvotes"] = data["imdbvotes"].replace(",", "")

    return data
