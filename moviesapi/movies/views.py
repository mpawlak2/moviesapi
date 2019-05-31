import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from movies.serializers import MovieSerializer
from movies.services import get_omdbapi_movie_by_title


class ListMoviesAPI(ListCreateAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        return []

    def create(self, request, *args, **kwargs):
        """The purpose of this override is to communicate with the external API and pass that data to the serializer."""
        serializer_data = {
            "title": request.data.get("title"),
        }

        if serializer_data["title"]:
            movie_data = get_omdbapi_movie_by_title(serializer_data["title"])
            serializer_data.update(
                {key.lower(): value for key, value in movie_data.items()},
            )


        serializer = self.get_serializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
