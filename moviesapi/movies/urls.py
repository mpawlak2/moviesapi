from django.urls import path

from movies.views import ListMoviesAPI


app_name = "movies"

urlpatterns = [
    path("movies/", ListMoviesAPI.as_view(), name="movies"),
]
