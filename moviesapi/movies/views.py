from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from movies.serializers import MovieSerializer


class ListMoviesAPI(ListCreateAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        return []
