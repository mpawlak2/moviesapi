from django.urls import path

from movies.views import MoviesAPI, CommentsAPI


app_name = "movies"

urlpatterns = [
    path("movies/", MoviesAPI.as_view(), name="movies"),
    path("comments/", CommentsAPI.as_view(), name="comments"),
]
