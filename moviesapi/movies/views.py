from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

import requests

from movies.serializers import MovieSerializer
from movies.services import get_omdbapi_movie_by_title


class ListMoviesAPI(ListCreateAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        return []

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        get_omdbapi_movie_by_title(title)
        return super().create(request, *args, **kwargs)
