from django.shortcuts import render
from rest_framework.generics import ListAPIView

from movies.serializers import MovieSerializer


class ListMoviesAPI(ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        return []
