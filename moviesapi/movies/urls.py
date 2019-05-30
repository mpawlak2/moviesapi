from django.urls import path

from movies.views import placeholder


app_name = "movies"

urlpatterns = [
    path("movies/", placeholder, name="movies"),
]
